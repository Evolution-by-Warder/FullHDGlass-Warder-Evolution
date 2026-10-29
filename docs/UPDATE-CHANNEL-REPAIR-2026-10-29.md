# Oprava ponuky aktualizácie TEST2 → 1.0.41

Nainštalovaný TEST2 vyberá podľa reťazca -test adresu warder-modernization-work/update-test.json. Tá zostala na migračnej 1.0.18, takže automatická ani ručná kontrola neponúkala 1.0.41. Produkčný feed bol správny, ale nevyriešil cestu už nainštalovaných TEST klientov.

update-test.json teraz ponúka presne overený produkčný balík 1.0.41 s rovnakou URL a SHA256 ako update-production.json. Publisher pri ďalších produkčných vydaniach aktivuje oba natívne kanály spolu. Rozlíšené sú aj očakávané verzie a prísne kontrolné súčty v inventári/verifikátoroch. Vydaný IPK ani jeho runtime sa nemenia.

Hlavný historický migračný most main/update.json zostáva bajtovo nezmenený na 1.0.18. Predmigračné legacy balíky musia najprv prejsť týmto mostom; natívny preinst naďalej odmieta nepripravenú legacy inštaláciu. Historický TEST alias sa už nesmie zamieňať s hlavným migračným kanálom.

Overenie musí vykonať skutočný výber kanála a ponuku v inštalovanej TEST2 ceste, nie iba načítať produkčný JSON. Grafika, 84 stĺpcov, farby, nastavenia aj fyzické balíky zostávajú nezmenené.
