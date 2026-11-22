#!/usr/bin/env python3
"""All 224 real Radio Browser countries: signed ZIP only, no old API downloads."""
import json
import string
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source/package-root/usr/lib/enigma2/python'))
from Plugins.Extensions.setupGlass17 import warderRadioLive as live
from Plugins.Extensions.setupGlass17 import warderRadioCountry as country
from Plugins.Extensions.setupGlass17 import warderRadioWorld as world

# Actual country IDs from the SHA-verified 224-country world of 2026-11-22.
REAL_CODES=(
    "AD AE AF AG AI AL AM AO AQ AR AS AT AU AW AZ BA BB BD BE BF BG BH BI BJ BM BN BO BQ "
    "BR BS BT BW BY BZ CA CC CD CF CG CH CI CL CM CN CO CR CU CV CW CX CY CZ DE DK DM DO "
    "DZ EC EE EG ER ES ET FI FJ FK FO FR GA GB GD GE GF GG GH GI GL GN GP GR GT GU GW GY "
    "HK HN HR HT HU ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN KP KR KW "
    "KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MG MH MK ML MM MN MO MQ MS MT MU "
    "MV MW MX MY MZ NA NC NE NG NI NL NO NP NU NZ OM PA PE PF PG PH PK PL PM PR PS PT PW "
    "PY QA RE RO RS RU RW SA SC SD SE SG SH SI SK SL SM SN SO SR SS SV SX SY TD TF TG TH "
    "TM TN TO TR TT TW TZ UA UG UM UN US UY UZ VA VC VE VG VI VN VU WF XK YE YT ZA ZM ZW"
).split()

class Call:
    def __init__(self,delay,cb):self.delay,self.cb=delay,cb
    def active(self):return True
    def cancel(self):pass

class Loop:
    def __init__(self):self.calls=[]
    def callLater(self,delay,cb):
        self.calls.append((delay,cb))
        return Call(delay,cb)

def controller(code, calls):
    c=live.Controller.__new__(live.Controller)
    c.closed=False;c.worker=None;c.pending=None;c.timeout=None;c.icon_worker=None
    c.icon_timer=None;c.world_worker=None;c.world_timer=None
    c.last_bulk_logo=None;c.local_world_sha=None;c.local_worker_key=None
    c.loop=Loop()
    c._observe_country_bouquet=lambda:code
    c._spawn=lambda mode,args,callback:calls.append((mode,args)) or object()
    return c

class Tests(unittest.TestCase):
    def test_exact_world_country_id_inventory(self):
        self.assertEqual(len(REAL_CODES),224)
        self.assertEqual(len(set(REAL_CODES)),224)
        self.assertIn('US',REAL_CODES)
        self.assertIn('SK',REAL_CODES)
        self.assertTrue(all(len(cc)==2 and cc.isalpha() and cc.isupper()
                            for cc in REAL_CODES))

    def test_all_224_missing_worlds_do_not_query_station_radio_browser(self):
        for cc in REAL_CODES:
            calls=[]
            c=controller(cc,calls)
            with patch.object(live,'_radio_world_root',return_value=Path('/tmp/hdg17_files')),\
                 patch.object(country,'_choice',return_value={'active':cc}),\
                 patch.object(country,'active_country',return_value=cc),\
                 patch.object(world,'cached_country',return_value=None):
                c.check()
            self.assertEqual(calls,[],cc)
            self.assertEqual(c.pending.delay,15,cc)

    def test_all_224_missing_worlds_do_not_download_individual_favicons(self):
        for cc in REAL_CODES:
            calls=[]
            c=controller(cc,calls)
            with patch.object(live,'_radio_world_root',return_value=Path('/tmp/hdg17_files')),\
                 patch.object(world,'cached_country',return_value=None):
                c.check_icon()
            self.assertEqual(calls,[],cc)
            self.assertEqual(c.icon_timer.delay,12,cc)

    def test_all_224_verified_countries_request_one_signed_original_zip(self):
        for cc in REAL_CODES:
            calls=[]
            c=controller(cc,calls)
            path=Path('/mnt/external/hdg17_files')
            with patch.object(live,'_radio_world_root',return_value=path),\
                 patch.object(live,'_radio_custom_picons_enabled',return_value=False),\
                 patch.object(world,'cached_country',return_value='b'*64):
                c.check_icon()
            self.assertEqual(calls,
                [('logo_zip',['--logos-world',cc,str(path)])],cc)

    def test_installer_and_country_worker_have_no_old_automatic_api_fallback(self):
        post=(ROOT/'source/control/postinst').read_text(encoding='utf-8')
        cli=(ROOT/'source/package-root/usr/lib/enigma2/python/'
             'Plugins/Extensions/setupGlass17/warderRadioCountry.py').read_text(encoding='utf-8')
        body=cli.split("if __name__ == '__main__':",1)[1]
        self.assertNotIn('"$warder_radio_country" --refresh',post)
        self.assertNotIn("sys.argv[1:] == ['--refresh']",body)
        self.assertNotIn("'--logos-online'",body)
        self.assertNotIn("sync_online_country(",body)
        self.assertIn("sync_selected_logos(",body)
        self.assertIn("900 if sys.argv[1:2] == ['--logos-world']",body)

if __name__=='__main__':
    unittest.main(verbosity=2)
