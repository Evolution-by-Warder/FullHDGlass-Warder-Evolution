#!/usr/bin/env python3
"""Unify shared native 23.5E picons with the existing Canal+ SK/CZ bytes."""
from pathlib import Path
import copy,hashlib,importlib.util,io,json,os,struct,tempfile,types,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('canal_audit',ROOT/'tools/audit-canal-overlap-20261101.py');audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
DATA=audit.DATA
sha=audit.sha


def normalized_name(filename,sync):
    stem=sync.normalize_service_reference(Path(filename).stem)
    return stem+'.png' if stem and sync.service_orbital_position(stem)=='23.5e' else None


def rewrite(package,original,canonical,sync):
    output=io.BytesIO();changes=[];old_hashes={};found=set()
    with zipfile.ZipFile(io.BytesIO(original)) as source:
        assert len(source.namelist())==len(set(source.namelist()))
        old_names=set(source.namelist())
        with zipfile.ZipFile(output,'w') as target:
            target.comment=source.comment
            for info in source.infolist():
                old=source.read(info);old_hashes[info.filename]=sha(old)
                name=normalized_name(info.filename,sync) if info.filename.lower().endswith('.png') else None
                if name:found.add(name)
                new=canonical.get(name,old)
                if old!=new:changes.append({'member':info.filename,'reference':name,'old_sha256':sha(old),'new_sha256':sha(new)})
                target.writestr(info,new)
            added=sorted(set(canonical)-found)
            for name in added:
                info=zipfile.ZipInfo(name,date_time=(2026,11,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.create_system=3;info.external_attr=0o100644<<16
                target.writestr(info,canonical[name])
    result=output.getvalue();changed_members={c['member'] for c in changes}
    with zipfile.ZipFile(io.BytesIO(result)) as z:
        assert set(z.namelist())==old_names|set(added)
        for name in old_names-changed_members:assert sha(z.read(name))==old_hashes[name],name
        for name in z.namelist():
            key=normalized_name(name,sync) if name.lower().endswith('.png') else None
            if key in canonical:assert z.read(name)==canonical[key],name
    return result,changes,added,len(old_names)-len(changes),len(old_names)+len(added)


def verify_receiver(document,loaded,records,reports):
    source=Path(os.environ['PICONHUB_RUNTIME'])
    namespace='canal_actual_receiver_verification';package=types.ModuleType(namespace);package.__path__=[str(source)];sys.modules[namespace]=package
    engine=__import__(namespace+'.warder_engine',fromlist=['PiconRunner']);sync=engine.sync
    docbytes=json.dumps(document).encode();metadata={p['filename']:p for p in document['parts']}
    all_urls={u for p in document['packages'] for u in p.get('parts',[])}
    def opener(url):
        if url==sync.RUNTIME_MANIFEST_URL:return io.BytesIO(docbytes)
        assert url in all_urls,url
        name=url.rsplit('/',1)[-1];path=DATA/name
        if not path.is_file():path=next((d/name for d in audit.PART_CACHES if (d/name).is_file()),None)
        assert path is not None and path.is_file(),name
        data=path.read_bytes();assert len(data)==metadata[name]['bytes'] and sha(data)==metadata[name]['sha256']
        return io.BytesIO(data)
    results=[]
    with tempfile.TemporaryDirectory(prefix='warder-canal-receiver-') as temp:
        folder=Path(temp);configs=[]
        for number,record in enumerate(reports):
            size,family=record['resolution'],record['family'];target=folder/str(number)/'picon'
            prefs=sync.set_task_position_bindings(sync.default_preferences(),[sync.task_binding_for_package_selector(s) for s in ('235E','CANALPLUS_SK','CANALPLUS_CZ')])
            prefs.update(resolution=size,style=family.removeprefix('channel-'),destination=str(target),update_mode=sync.UPDATE_MODE_INCREMENTAL)
            events=[];runner=engine.PiconRunner(opener=opener,event=lambda *a:events.append(a),enigma2_dir=str(folder/'enigma2'),lock_path=str(folder/'lock'))
            result=runner.run([prefs])
            canonical=dict(loaded[(size,family,'CANALPLUS_SK')]['images']);canonical.update(loaded[(size,family,'CANALPLUS_CZ')]['images'])
            assert all((target/name).read_bytes()==png for name,png in canonical.items())
            assert sum(e[0]=='processed' for e in events)==3
            configs.append(prefs)
            results.append({'resolution':size,'family':family,'combined_three_selectors':'passed','result':result,'canonical_provider_picons_verified':len(canonical)})
            print('RECEIVER VERIFIED',size,family,result,flush=True)
        prefs=next(p for p in configs if p['resolution']=='220x132' and p['style']=='black')
        runner=engine.PiconRunner(opener=opener,enigma2_dir=str(folder/'enigma2'),lock_path=str(folder/'lock'))
        repeated=runner.run([prefs]);assert repeated=={'added':0,'changed':0,'removed':0},repeated
        canonical=loaded[('220x132','channel-black','CANALPLUS_CZ')]['images'];png=next(iter(canonical.values()))
        stale='1_0_1_FFFD_FFFE_3_EB0000_0_0_0.png';foreign='1_0_1_FFFD_FFFE_3_C00000_0_0_0.png'
        target=Path(prefs['destination']);(target/stale).write_bytes(png);(target/foreign).write_bytes(png)
        replacement=dict(prefs,update_mode=sync.UPDATE_MODE_REPLACE_ALL)
        result=runner.run([replacement]);assert result=={'added':0,'changed':0,'removed':1},result
        assert not (target/stale).exists() and (target/foreign).read_bytes()==png
        e2=folder/'enigma2';e2.mkdir()
        chosen=list(sorted(canonical))[:2]
        (e2/'bouquets.tv').write_text('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.canal.tv" ORDER BY bouquet\n')
        (e2/'userbouquet.canal.tv').write_text(''.join('#SERVICE '+n[:-4].replace('_',':')+':\n' for n in chosen))
        selective=dict(prefs,destination=str(folder/'selective'/'picon'),update_mode=sync.UPDATE_MODE_SYNC_TV)
        selective_result=runner.run([selective]);assert selective_result['added']==2,selective_result
        assert set(p.name for p in Path(selective['destination']).glob('*.png'))==set(chosen)
        batch=[dict(prefs,destination=str(folder/'batch1'/'picon'),profile_number=1),dict(next(p for p in configs if p['resolution']=='50x30' and p['style']=='white'),destination=str(folder/'batch3'/'picon'),profile_number=3)]
        batch_result=runner.run(batch);assert batch_result['added']>0 and batch_result['removed']==0
    return {'variants':results,'incremental_second_run':repeated,'replace_mode_preserves_foreign_position':True,'tv_bouquet_sync':'passed','two_independent_profile_batch':'passed','receiver_hardware_test':False}


def write_summary(report):
    lines=['# 23.5E / Canal+ SK / Canal+ CZ — zjednotenie piconov', '',
           'Spoločné picony v plných balíkoch 23,5°E používajú presné pôvodné PNG bajty z navzájom zhodných Canal+ SK/CZ balíkov. Kontroluje sa technická referencia a orbitálna pozícia, nie iba názov stanice. Cudzie orbitálne aliasy sa nemenia.', '',
           '| Rozlíšenie | Pozadie | Zjednotené PNG | Doplnené referencie | Ostatné pôvodné PNG zachované |',
           '|---|---|---:|---:|---:|']
    for item in report['packages']:
        lines.append('| %s | %s | %d | %d | %d |'%(item['resolution'],item['family'].removeprefix('channel-'),len(item['replaced']),len(item['added']),item['unrelated_pngs_preserved']))
    lines.extend(['',
        'Celkovo: %d zjednotených PNG a %d doplnených referencií naprieč %d variantmi. Počty obrázkov neznamenajú rovnaký počet staníc, pretože zahŕňajú rozlíšenia, pozadia a technické aliasy.'%(report['replaced_pngs'],report['added_native_pngs'],report['package_variants']), '',
        'Ostatných %d balíkov aj oba zdrojové Canal+ balíky zostávajú zachované. Staré publikované archívy zostávajú dostupné pod pôvodnými názvami.'%report['unrelated_packages_preserved'], '',
        '## Overenie', '',
        '- Skutočný sťahovací a inštalačný engine PiconHub 0.1.38 úspešne spracoval všetky tri selektory naraz vo všetkých deviatich variantoch.',
        '- Druhý inkrementálny beh: 0 pridaných, 0 zmenených, 0 odstránených.',
        '- Úplné nahradenie odstránilo skúšobnú neaktuálnu referenciu 23,5°E a zachovalo picon inej orbitálnej pozície.',
        '- Synchronizácia podľa TV bouquetu aj dávka dvoch samostatných profilov prešli.',
        '- Pri každom archíve sa overili SHA256 jeho častí, celého ZIPu a všetky pôvodné i nové PNG bajty.',
        '- Výsledky sú hostiteľské testy s reálnym enginom; overenie na fyzickom prijímači zostáva na používateľovi.', '',
        '## Použitie', '',
        'Po zverejnení do produkčného katalógu stačí znovu spustiť sťahovanie piconov. Nové IPK ani zmena nastavení profilov nie sú potrebné. Táto dátová oprava nemení stabilný aktualizačný kanál pluginu.', '',
        'Podrobné referencie a pôvodné/nové SHA256: [canal-unification-20261101.json](canal-unification-20261101.json).', ''])
    (ROOT/'reports/CANAL-UNIFICATION-20261101.md').write_text('\n'.join(lines))


def main():
    manifest=DATA/'manifest.json';before=json.loads(manifest.read_text());doc=copy.deepcopy(before)
    loaded,groups=audit.audit(before);sync=audit.load_sync();metadata={p['filename']:p for p in before['parts']}
    assert len(groups)==9
    assert all(not g['provider_conflicts'] for g in groups),'Provider sources disagree; review needed'
    assert all(not g['invalid_native_images'] for g in groups),'Invalid native source PNG; review needed'
    reports=[];new_meta=[];old_parts=set();changed_keys=set()
    for group in groups:
        size,family=group['resolution'],group['family'];full=loaded[(size,family,'235E')];sk=loaded[(size,family,'CANALPLUS_SK')];cz=loaded[(size,family,'CANALPLUS_CZ')]
        canonical=dict(sk['images']);canonical.update(cz['images'])
        raw=audit.read_archive(full['package'],metadata)
        packed,changes,added,preserved,png_count=rewrite(full['package'],raw,canonical,sync)
        assert len(set(c['reference'] for c in changes))==len(group['replacements'])
        assert added==group['missing_from_full']
        digest=sha(packed);filename='warder-235e-'+size+'-'+family.removeprefix('channel-')+'-'+digest[:16]+'.zip'
        package=next(p for p in doc['packages'] if (p['selector_id'],p['resolution'],p['family'])==('235E',size,family))
        prefix=package['parts'][0].rsplit('/',1)[0]+'/';urls=[]
        for number,start in enumerate(range(0,len(packed),4*1024*1024)):
            name=filename+'.part%02d'%number;data=packed[start:start+4*1024*1024];(DATA/name).write_bytes(data);urls.append(prefix+name)
            new_meta.append({'filename':name,'bytes':len(data),'sha256':sha(data)})
        old_parts.update(u.rsplit('/',1)[-1] for u in package['parts'])
        package.update(filename=filename,bytes=len(packed),sha256=digest,parts=urls,png_count=png_count)
        if 'included_references' in package:
            with zipfile.ZipFile(io.BytesIO(packed)) as z:package['included_references']=sorted(Path(n).name[:-4] for n in z.namelist() if n.lower().endswith('.png'))
        package['canal_overlap_unification_20261101']={'source_packages':{sid:loaded[(size,family,sid)]['package']['sha256'] for sid in ('CANALPLUS_SK','CANALPLUS_CZ')},'replaced':len(changes),'added':len(added),'unrelated_pngs_preserved':preserved}
        changed_keys.add(('235E',size,family))
        reports.append({'resolution':size,'family':family,'old_archive_sha256':full['package']['sha256'],'archive_sha256':digest,'archive_filename':filename,'bytes':len(packed),'png_count':png_count,'replaced':changes,'added':[{'reference':n,'sha256':sha(canonical[n])} for n in added],'unrelated_pngs_preserved':preserved,'all_shared_native_pngs_identical':True,'canal_source_packages':package['canal_overlap_unification_20261101']['source_packages']})
        print('UNIFIED',size,family,len(changes),'replaced',len(added),'added',flush=True)
    doc['parts']=[p for p in doc['parts'] if p['filename'] not in old_parts]+new_meta
    untouched_before=[p for p in before['packages'] if (p['selector_id'],p['resolution'],p['family']) not in changed_keys]
    untouched_after=[p for p in doc['packages'] if (p['selector_id'],p['resolution'],p['family']) not in changed_keys]
    assert untouched_before==untouched_after
    assert sync.validate_publication_manifest(doc,'production')==[]
    checks=verify_receiver(doc,loaded,new_meta,reports)
    manifest.write_text(json.dumps(doc,sort_keys=True,indent=2)+'\n')
    sums=DATA/'SHA256SUMS';values={line.split()[-1]:line.split()[0] for line in sums.read_text().splitlines() if line.strip()}
    values.update({p['filename']:p['sha256'] for p in new_meta});values['manifest.json']=sha(manifest.read_bytes())
    sums.write_text(''.join(h+'  '+n+'\n' for n,h in sorted(values.items())))
    report={'policy':'Copy existing identical Canal+ SK/CZ native 23.5E PNG bytes to full-position packages; retain all unrelated artwork and published archives.','package_variants':len(reports),'replaced_pngs':sum(len(r['replaced']) for r in reports),'added_native_pngs':sum(len(r['added']) for r in reports),'unrelated_packages_preserved':len(untouched_before),'canal_provider_packages_unchanged':True,'other_positions_unchanged':True,'old_immutable_archives_preserved':True,'ipk_changed':False,'packages':reports,'receiver_checks':checks}
    (ROOT/'reports/canal-unification-20261101.json').write_text(json.dumps(report,indent=2)+'\n')
    write_summary(report)
    print('COMPLETE',json.dumps({k:report[k] for k in ('package_variants','replaced_pngs','added_native_pngs','unrelated_packages_preserved')}),flush=True)


if __name__=='__main__':main()
