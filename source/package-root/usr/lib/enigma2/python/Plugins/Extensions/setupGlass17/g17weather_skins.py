skinWea = {}
skinWea["1"] = """<screen name="WeatherScreen" position="645,163" size="1177,487" title="Weather" zPosition="8" backgroundColor="background" >                                           

<widget name="Weather_items" font="Prive3;25" position="0,0" zPosition="2" size="247,300" valign="top" halign="right" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_values" font="Prive3;25" position="262,0" zPosition="3" size="300,300" valign="top" halign="left"  backgroundColor="background" transparent="1" />

<widget name="Weather_picon0" pixmap="hd_glass17/icons/3200.png" position="532,52" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperature0" font="Prive3;31" position="474,168" zPosition="2" size="225,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state0" font="Prive3;24" position="474,0" zPosition="3" size="225,52" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<eLabel position="7,213" zPosition="8" size="1162,1" backgroundColor="#1546AF" transparent="0" />

<widget name="Weather_wind" pixmap="hd_glass17/icons/no-wind.png" position="712,0" zPosition="5" size="208,208" alphatest="blend" />
<widget name="Weather_wind_label" font="Prive3;27" position="708,7" zPosition="2" size="0,0" valign="center" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_sunrise" font="Prive3;24" position="937,78" zPosition="5" size="225,30" valign="top" halign="center" foregroundColor="#ffcc00" backgroundColor="background" transparent="1" />
<widget name="Weather_sunset" font="Prive3;24" position="937,186" zPosition="5" size="225,30" valign="top" halign="center" foregroundColor="#ff3300" backgroundColor="background" transparent="1" />
<ePixmap position="975,0" zPosition="6" size="148,75" pixmap="hd_glass17/icons/Sunrise-fs8.png" alphatest="blend"/>
<ePixmap position="975,108" zPosition="6" size="148,75" pixmap="hd_glass17/icons/Sunset-fs8.png" alphatest="blend"/>

<widget name="Weather_picon1" pixmap="hd_glass17/icons/3200.png" position="67,277" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow1" font="Prive3;31" position="22,390" zPosition="2" size="97,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature1" font="Prive3;31" position="120,390" zPosition="2" size="97,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state1" font="Prive3;24" position="7,225" zPosition="3" size="225,52" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date1" font="Prive3;24" position="7,427" zPosition="3" size="225,52" valign="top" halign="center"  foregroundColor="#CC3399" backgroundColor="background" transparent="1" />

<widget name="Weather_picon2" pixmap="hd_glass17/icons/3200.png" position="300,277" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow2" font="Prive3;31" position="255,390" zPosition="2" size="97,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature2" font="Prive3;31" position="352,390" zPosition="2" size="97,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state2" font="Prive3;24" position="240,225" zPosition="3" size="225,52" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date2" font="Prive3;24" position="240,427" zPosition="3" size="225,52" valign="top" halign="center"  foregroundColor="#CC3399" backgroundColor="background" transparent="1" />

<widget name="Weather_picon3" pixmap="hd_glass17/icons/3200.png" position="532,277" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow3" font="Prive3;31" position="487,390" zPosition="2" size="97,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature3" font="Prive3;31" position="585,390" zPosition="2" size="97,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state3" font="Prive3;24" position="472,225" zPosition="3" size="225,52" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date3" font="Prive3;24" position="472,427" zPosition="3" size="225,52" valign="top" halign="center"  foregroundColor="#CC3399" backgroundColor="background" transparent="1" />

<widget name="Weather_picon4" pixmap="hd_glass17/icons/3200.png" position="765,277" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow4" font="Prive3;31" position="720,390" zPosition="2" size="97,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature4" font="Prive3;31" position="817,390" zPosition="2" size="97,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state4" font="Prive3;24" position="705,225" zPosition="3" size="225,52" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date4" font="Prive3;24" position="705,427" zPosition="3" size="225,52" valign="top" halign="center"  foregroundColor="#CC3399" backgroundColor="background" transparent="1" />

<widget name="Weather_picon5" pixmap="hd_glass17/icons/3200.png" position="997,277" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow5" font="Prive3;31" position="952,390" zPosition="2" size="97,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature5" font="Prive3;31" position="1050,390" zPosition="2" size="97,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state5" font="Prive3;24" position="937,225" zPosition="3" size="225,52" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date5" font="Prive3;24" position="937,427" zPosition="3" size="225,52" valign="top" halign="center"  foregroundColor="#CC3399" backgroundColor="background" transparent="1" />

<widget name="moon_pict" position="1010,29" zPosition="5" size="0,0" alphatest="blend" />
<widget name="moon_phase" font="Prive3;24" position="952,176" zPosition="3" size="0,0" valign="top" halign="center" foregroundColor="#00d100" backgroundColor="background" transparent="1" />

</screen>"""

skinWea["2"] = """<screen name="WeatherScreen" position="832,150" size="990,502" zPosition="8" title="Weather" backgroundColor="background" >                                           
<widget name="Weather_sunrise" font="Prive3;33" position="1275,237" zPosition="5" size="0,0" valign="top" halign="center" foregroundColor="#66CCFF" backgroundColor="background" transparent="1" />
<widget name="Weather_wind" pixmap="hd_glass17/icons/no-wind.png" position="975,60" zPosition="5" size="0,0" alphatest="blend" />
<widget name="Weather_wind_label" font="Prive3;33" position="855,7" zPosition="2" size="0,0" valign="center" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_picon1" pixmap="hd_glass17/icons/3200.png" position="105,382" zPosition="5" size="0,0" alphatest="blend" />
<widget name="Weather_state1" font="Prive3;33" position="7,303" zPosition="3" size="0,0" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date1" font="Prive3;33" position="7,540" zPosition="3" size="0,0" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_sunset" font="Prive3;33" position="15,0" zPosition="2" size="310,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature0" font="Prive3;60" position="30,60" zPosition="2" size="150,67" valign="top" halign="left" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_picon0" pixmap="hd_glass17/icons/3200.png" position="195,45" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_state0" font="Prive3;25" position="15,157" zPosition="3" size="300,52" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<eLabel text="Max:" font="Prive3;27" position="22,210" zPosition="2" size="75,60" valign="top" halign="left" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature1" font="Prive3;27" position="105,210" zPosition="2" size="105,60" valign="top" halign="left" foregroundColor="red" backgroundColor="background" transparent="1" />
<eLabel text="Min:" font="Prive3;27" position="195,210" zPosition="2" size="75,60" valign="top" halign="left" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperaturelow1" font="Prive3;27" position="277,210" zPosition="2" size="112,60" valign="top" halign="left" foregroundColor="blue" backgroundColor="background" transparent="1" />

<widget name="Weather_items" font="Prive3;25" position="375,7" zPosition="2" size="310,345" valign="top" halign="right" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_values" font="Prive3;25" position="700,7" zPosition="3" size="450,345" valign="top" halign="left"  backgroundColor="background" transparent="1" />
<eLabel position="7,262" zPosition="8" size="1530,1" backgroundColor="#1546AF" transparent="0" />

<widget name="Weather_state2" font="Prive3;25" position="15,270" zPosition="3" size="300,52" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_picon2" pixmap="hd_glass17/icons/3200.png" position="15,325" zPosition="5" size="108,108" alphatest="blend" />
<ePixmap position="135,348" zPosition="7" size="28,24" pixmap="hd_glass17/icons/up.png" alphatest="on"/>
<widget name="Weather_Temperature2" font="Prive3;31" position="172,337" zPosition="2" size="112,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<ePixmap position="135,390" zPosition="7" size="28,24" pixmap="hd_glass17/icons/down.png" alphatest="on"/>
<widget name="Weather_Temperaturelow2" font="Prive3;31" position="172,379" zPosition="2" size="112,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Date2" font="Prive3;25" position="15,441" zPosition="3" size="300,52" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_state3" font="Prive3;25" position="352,270" zPosition="3" size="300,52" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_picon3" pixmap="hd_glass17/icons/3200.png" position="352,325" zPosition="5" size="108,108" alphatest="blend" />
<ePixmap position="472,348" zPosition="7" size="28,24" pixmap="hd_glass17/icons/up.png" alphatest="on"/>
<widget name="Weather_Temperature3" font="Prive3;31" position="510,337" zPosition="2" size="112,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<ePixmap position="472,390" zPosition="7" size="28,24" pixmap="hd_glass17/icons/down.png" alphatest="on"/>
<widget name="Weather_Temperaturelow3" font="Prive3;31" position="510,379" zPosition="2" size="112,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Date3" font="Prive3;25" position="352,441" zPosition="3" size="300,52" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_state4" font="Prive3;25" position="675,270" zPosition="3" size="300,52" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_picon4" pixmap="hd_glass17/icons/3200.png" position="675,325" zPosition="5" size="108,108" alphatest="blend" />
<ePixmap position="795,348" zPosition="7" size="28,24" pixmap="hd_glass17/icons/up.png" alphatest="on"/>
<widget name="Weather_Temperature4" font="Prive3;31" position="832,337" zPosition="2" size="112,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<ePixmap position="795,390" zPosition="7" size="28,24" pixmap="hd_glass17/icons/down.png" alphatest="on"/>
<widget name="Weather_Temperaturelow4" font="Prive3;31" position="832,379" zPosition="2" size="112,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Date4" font="Prive3;25" position="675,441" zPosition="3" size="300,52" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_picon5" pixmap="hd_glass17/icons/3200.png" position="997,277" zPosition="5" size="0,0" alphatest="blend" />
<widget name="Weather_Temperaturelow5" font="Prive3;31" position="952,390" zPosition="2" size="0,0" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature5" font="Prive3;31" position="1050,390" zPosition="2" size="0,0" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state5" font="Prive3;24" position="937,225" zPosition="3" size="0,0" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date5" font="Prive3;24" position="937,427" zPosition="3" size="0,0" valign="top" halign="center"  foregroundColor="#CC3399" backgroundColor="background" transparent="1" />

<widget name="moon_pict" position="1010,29" zPosition="5" size="0,0" alphatest="blend" />
<widget name="moon_phase" font="Prive3;24" position="952,176" zPosition="3" size="0,0" valign="top" halign="center" foregroundColor="#00d100" backgroundColor="background" transparent="1" />

</screen>"""

skinWea["3"] = """<screen name="WeatherScreen" position="center,120" size="1545,645" zPosition="8" title="Weather" backgroundColor="background" >                                           

<widget name="Weather_items" font="Prive3;33" position="0,15" zPosition="2" size="310,300" valign="top" halign="right" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_values" font="Prive3;33" position="325,15" zPosition="3" size="450,300" valign="top" halign="left"  backgroundColor="background" transparent="1" />

<widget name="Weather_picon0" pixmap="hd_glass17/icons/3200.png" position="720,90" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperature0" font="Prive3;37" position="622,217" zPosition="2" size="300,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state0" font="Prive3;33" position="622,7" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<eLabel position="7,289" zPosition="8" size="1530,1" backgroundColor="#1546AF" transparent="0" />

<widget name="Weather_wind" pixmap="hd_glass17/icons/no-wind.png" position="975,60" zPosition="5" size="208,208" alphatest="blend" />
<widget name="Weather_wind_label" font="Prive3;33" position="855,7" zPosition="2" size="450,45" valign="center" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_sunrise" font="Prive3;33" position="1275,102" zPosition="5" size="225,37" valign="top" halign="center" foregroundColor="#ffcc00" backgroundColor="background" transparent="1" />
<widget name="Weather_sunset" font="Prive3;33" position="1275,237" zPosition="5" size="225,37" valign="top" halign="center" foregroundColor="#ff3300" backgroundColor="background" transparent="1" />
<ePixmap position="1312,15" zPosition="6" size="148,75" pixmap="hd_glass17/icons/Sunrise-fs8.png" alphatest="blend"/>
<ePixmap position="1312,150" zPosition="6" size="148,75" pixmap="hd_glass17/icons/Sunset-fs8.png" alphatest="blend"/>

<widget name="Weather_picon1" pixmap="hd_glass17/icons/3200.png" position="105,382" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow1" font="Prive3;36" position="45,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature1" font="Prive3;37" position="157,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state1" font="Prive3;33" position="7,303" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date1" font="Prive3;33" position="7,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_picon2" pixmap="hd_glass17/icons/3200.png" position="412,382" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow2" font="Prive3;36" position="352,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature2" font="Prive3;37" position="465,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state2" font="Prive3;33" position="315,303" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date2" font="Prive3;33" position="315,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_picon3" pixmap="hd_glass17/icons/3200.png" position="720,382" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow3" font="Prive3;36" position="660,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature3" font="Prive3;37" position="772,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state3" font="Prive3;33" position="622,303" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date3" font="Prive3;33" position="622,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_picon4" pixmap="hd_glass17/icons/3200.png" position="1027,382" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow4" font="Prive3;36" position="967,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature4" font="Prive3;37" position="1080,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state4" font="Prive3;33" position="930,303" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date4" font="Prive3;33" position="930,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_picon5" pixmap="hd_glass17/icons/3200.png" position="1335,382" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow5" font="Prive3;36" position="1275,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature5" font="Prive3;37" position="1387,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state5" font="Prive3;33" position="1237,303" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date5" font="Prive3;33" position="1237,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="moon_pict" position="1010,29" zPosition="5" size="0,0" alphatest="blend" />
<widget name="moon_phase" font="Prive3;24" position="952,176" zPosition="3" size="0,0" valign="top" halign="center" foregroundColor="#00d100" backgroundColor="background" transparent="1" />

</screen>"""

skinWea["4"] = """<screen name="WeatherScreen" position="center,120" size="990,645" zPosition="8" title="Weather" backgroundColor="background" >                                           
<widget name="Weather_sunrise" font="Prive3;33" position="1275,237" zPosition="5" size="0,0" valign="top" halign="center" foregroundColor="#66CCFF" backgroundColor="background" transparent="1" />
<widget name="Weather_wind" pixmap="hd_glass17/icons/no-wind.png" position="975,60" zPosition="5" size="0,0" alphatest="blend" />
<widget name="Weather_wind_label" font="Prive3;33" position="855,7" zPosition="2" size="0,0" valign="center" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_picon1" pixmap="hd_glass17/icons/3200.png" position="105,382" zPosition="5" size="0,0" alphatest="blend" />
<widget name="Weather_state1" font="Prive3;33" position="7,303" zPosition="3" size="0,0" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date1" font="Prive3;33" position="7,540" zPosition="3" size="0,0" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_sunset" font="Prive3;37" position="15,15" zPosition="2" size="310,45" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature0" font="Prive3;75" position="15,67" zPosition="2" size="150,90" valign="top" halign="left" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_picon0" pixmap="hd_glass17/icons/3200.png" position="195,67" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_state0" font="Prive3;33" position="15,180" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<eLabel text="Max:" font="Prive3;30" position="15,255" zPosition="2" size="75,60" valign="top" halign="left" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature1" font="Prive3;30" position="105,255" zPosition="2" size="105,60" valign="top" halign="left" foregroundColor="red" backgroundColor="background" transparent="1" />
<eLabel text="Min:" font="Prive3;30" position="195,255" zPosition="2" size="75,60" valign="top" halign="left" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperaturelow1" font="Prive3;30" position="285,255" zPosition="2" size="112,60" valign="top" halign="left" foregroundColor="blue" backgroundColor="background" transparent="1" />

<widget name="Weather_items" font="Prive3;30" position="375,7" zPosition="2" size="310,345" valign="top" halign="right" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_values" font="Prive3;30" position="700,7" zPosition="3" size="450,345" valign="top" halign="left"  backgroundColor="background" transparent="1" />
<eLabel position="7,322" zPosition="8" size="1530,1" backgroundColor="#1546AF" transparent="0" />

<widget name="Weather_state2" font="Prive3;33" position="15,345" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_picon2" pixmap="hd_glass17/icons/3200.png" position="15,424" zPosition="5" size="108,108" alphatest="blend" />
<ePixmap position="135,435" zPosition="7" size="28,24" pixmap="hd_glass17/icons/up.png" alphatest="on"/>
<widget name="Weather_Temperature2" font="Prive3;37" position="172,424" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<ePixmap position="135,487" zPosition="7" size="28,24" pixmap="hd_glass17/icons/down.png" alphatest="on"/>
<widget name="Weather_Temperaturelow2" font="Prive3;36" position="172,477" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Date2" font="Prive3;33" position="15,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_state3" font="Prive3;33" position="352,345" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_picon3" pixmap="hd_glass17/icons/3200.png" position="352,424" zPosition="5" size="108,108" alphatest="blend" />
<ePixmap position="472,435" zPosition="7" size="28,24" pixmap="hd_glass17/icons/up.png" alphatest="on"/>
<widget name="Weather_Temperature3" font="Prive3;37" position="510,424" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<ePixmap position="472,487" zPosition="7" size="28,24" pixmap="hd_glass17/icons/down.png" alphatest="on"/>
<widget name="Weather_Temperaturelow3" font="Prive3;36" position="510,477" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Date3" font="Prive3;33" position="352,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_state4" font="Prive3;33" position="675,345" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_picon4" pixmap="hd_glass17/icons/3200.png" position="675,424" zPosition="5" size="108,108" alphatest="blend" />
<ePixmap position="795,435" zPosition="7" size="28,24" pixmap="hd_glass17/icons/up.png" alphatest="on"/>
<widget name="Weather_Temperature4" font="Prive3;37" position="832,424" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<ePixmap position="795,487" zPosition="7" size="28,24" pixmap="hd_glass17/icons/down.png" alphatest="on"/>
<widget name="Weather_Temperaturelow4" font="Prive3;36" position="832,477" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Date4" font="Prive3;33" position="675,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_picon5" pixmap="hd_glass17/icons/3200.png" position="1335,382" zPosition="5" size="0,0" alphatest="blend" />
<widget name="Weather_Temperaturelow5" font="Prive3;36" position="1275,495" zPosition="2" size="0,0" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature5" font="Prive3;37" position="1387,495" zPosition="2" size="0,0" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state5" font="Prive3;33" position="1237,303" zPosition="3" size="0,0" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date5" font="Prive3;33" position="1237,540" zPosition="3" size="0,0" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="moon_pict" position="1010,29" zPosition="5" size="0,0" alphatest="blend" />
<widget name="moon_phase" font="Prive3;24" position="952,176" zPosition="3" size="0,0" valign="top" halign="center" foregroundColor="#00d100" backgroundColor="background" transparent="1" />

</screen>"""

skinWea["5"] = """<screen name="WeatherScreen" position="0,0" size="1920,1080" zPosition="8" title="Weather" backgroundColor="black" flags="wfNoBorder" >                                                                                              
<widget source="Title" render="Label" position="174,96" size="1570,49" zPosition="1" font="Prive3;37" halign="center" transparent="1" foregroundColor="#00ff8000" shadowColor="#1A58A6" shadowOffset="-2,-1" />
<widget name="Weather_items" font="Prive3;30" position="154,225" zPosition="2" size="315,300" valign="top" halign="right" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_values" font="Prive3;30" position="484,225" zPosition="3" size="315,300" valign="top" halign="left"  backgroundColor="background" transparent="1" />

<widget name="Weather_picon0" pixmap="hd_glass17/icons/3200.png" position="862,270" zPosition="1" size="192,192" transparent="1" alphatest="blend" />
<widget name="Weather_Temperature0" font="Regular;34" position="862,477" zPosition="3" size="192,60" valign="center" halign="center" foregroundColor="#cc3300" backgroundColor="background" transparent="1" />
<widget name="Weather_state0" font="Prive3;30" position="808,165" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_wind" position="1500,268" zPosition="5" size="208,208" alphatest="blend" />
<widget name="Weather_wind_label" font="Prive3;30" position="1380,165" zPosition="2" size="450,84" valign="center" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_sunrise" font="Prive3;30" position="1135,165" zPosition="5" size="150,84" valign="center" halign="center" foregroundColor="#ffcc00" backgroundColor="background" transparent="1" />
<widget name="Weather_sunset" font="Prive3;30" position="1285,165" zPosition="5" size="150,84" valign="center" halign="center" foregroundColor="#ff3300" backgroundColor="background" transparent="1" />
<ePixmap position="1135,366" zPosition="6" size="148,75" pixmap="hd_glass17/icons/Sunrise-fs8.png" alphatest="blend"/>
<ePixmap position="1285,366" zPosition="6" size="148,75" pixmap="hd_glass17/icons/Sunset-fs8.png" alphatest="blend"/>

<widget name="Weather_picon1" pixmap="hd_glass17/icons/3200.png" position="208,630" zPosition="1" size="192,192" transparent="1" alphatest="blend" backgroundColor="background" />
<widget name="Weather_Temperaturelow1" font="Regular;34" position="208,832" zPosition="2" size="96,60" valign="center" halign="center" foregroundColor="blue" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature1" font="Regular;34" position="304,832" zPosition="2" size="96,60" valign="center" halign="center" foregroundColor="#cc3300" backgroundColor="background" transparent="1" />
<widget name="Weather_state1" font="Prive3;30" position="154,540" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date1" font="Prive3;30" position="154,897" zPosition="3" size="300,66" valign="top" halign="center"  foregroundColor="#26cfc0" backgroundColor="background" transparent="1" />

<widget name="Weather_picon2" pixmap="hd_glass17/icons/3200.png" position="535,630" zPosition="1" size="192,192" transparent="1" alphatest="blend" />
<widget name="Weather_Temperaturelow2" font="Regular;34" position="535,832" zPosition="2" size="96,60" valign="center" halign="center" foregroundColor="blue" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature2" font="Regular;34" position="631,832" zPosition="2" size="96,60" valign="center" halign="center" foregroundColor="#cc3300" backgroundColor="background" transparent="1" />
<widget name="Weather_state2" font="Prive3;30" position="481,540" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date2" font="Prive3;30" position="481,897" zPosition="3" size="300,66" valign="top" halign="center"  foregroundColor="#26cfc0" backgroundColor="background" transparent="1" />

<widget name="Weather_picon3" pixmap="hd_glass17/icons/3200.png" position="862,630" zPosition="1" size="192,192" transparent="1" alphatest="blend" />
<widget name="Weather_Temperaturelow3" font="Regular;34" position="862,832" zPosition="2" size="96,60" valign="center" halign="center" foregroundColor="blue" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature3" font="Regular;34" position="958,832" zPosition="2" size="96,60" valign="center" halign="center" foregroundColor="#cc3300" backgroundColor="background" transparent="1" />
<widget name="Weather_state3" font="Prive3;30" position="808,540" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date3" font="Prive3;30" position="808,897" zPosition="3" size="300,66" valign="top" halign="center"  foregroundColor="#26cfc0" backgroundColor="background" transparent="1" />

<widget name="Weather_picon4" pixmap="hd_glass17/icons/3200.png" position="1189,630" zPosition="1" size="192,192" transparent="1" alphatest="blend" />
<widget name="Weather_Temperaturelow4" font="Regular;34" position="1189,832" zPosition="2" size="96,60" valign="center" halign="center" foregroundColor="blue" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature4" font="Regular;34" position="1285,832" zPosition="2" size="96,60" valign="center" halign="center" foregroundColor="#cc3300" backgroundColor="background" transparent="1" />
<widget name="Weather_state4" font="Prive3;30" position="1135,540" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date4" font="Prive3;30" position="1135,897" zPosition="3" size="300,66" valign="top" halign="center"  foregroundColor="#26cfc0" backgroundColor="background" transparent="1" />

<widget name="Weather_picon5" pixmap="hd_glass17/icons/3200.png" position="1516,630" zPosition="1" size="192,192" transparent="1" alphatest="blend" />
<widget name="Weather_Temperaturelow5" font="Regular;34" position="1516,832" zPosition="2" size="96,60" valign="center" halign="center" foregroundColor="blue" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature5" font="Regular;34" position="1612,832" zPosition="2" size="96,60" valign="center" halign="center" foregroundColor="#cc3300" backgroundColor="background" transparent="1" />
<widget name="Weather_state5" font="Prive3;30" position="1462,540" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date5" font="Prive3;30" position="1462,897" zPosition="3" size="300,66" valign="top" halign="center"  foregroundColor="#26cfc0" backgroundColor="background" transparent="1" />

<widget name="moon_pict" position="1010,29" zPosition="5" size="0,0" alphatest="blend" />
<widget name="moon_phase" font="Prive3;24" position="952,176" zPosition="3" size="0,0" valign="top" halign="center" foregroundColor="#00d100" backgroundColor="background" transparent="1" />

</screen>"""

skinWea["6"] = """<screen name="WeatherScreen" position="center,120" size="1545,645" zPosition="8" title="Weather" backgroundColor="black" >                                           

<widget name="Weather_items" font="Prive3;33" position="0,15" zPosition="2" size="310,300" valign="top" halign="right" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_values" font="Prive3;33" position="325,15" zPosition="3" size="450,300" valign="top" halign="left"  backgroundColor="black" transparent="1" />

<widget name="Weather_picon0" pixmap="hd_glass17/icons/3200.png" position="720,90" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperature0" font="Prive3;65" position="622,207" zPosition="2" size="300,70" valign="top" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_state0" font="Prive3;33" position="622,7" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="black" transparent="1" />
<eLabel position="7,289" zPosition="8" size="1530,1" backgroundColor="#1546AF" transparent="0" />

<widget name="Weather_wind" pixmap="hd_glass17/icons/no-wind.png" position="975,60" zPosition="5" size="208,208" alphatest="blend" />
<widget name="Weather_wind_label" font="Prive3;33" position="855,7" zPosition="2" size="450,45" valign="center" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_sunrise" font="Prive3;33" position="1275,102" zPosition="5" size="225,37" valign="top" halign="center" foregroundColor="#ffcc00" backgroundColor="black" transparent="1" />
<widget name="Weather_sunset" font="Prive3;33" position="1275,237" zPosition="5" size="225,37" valign="top" halign="center" foregroundColor="#ff3300" backgroundColor="black" transparent="1" />
<ePixmap position="1312,15" zPosition="6" size="148,75" pixmap="hd_glass17/icons/Sunrise-fs8.png" alphatest="blend"/>
<ePixmap position="1312,150" zPosition="6" size="148,75" pixmap="hd_glass17/icons/Sunset-fs8.png" alphatest="blend"/>

<widget name="Weather_picon1" pixmap="hd_glass17/icons/3200.png" position="105,382" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow1" font="Prive3;36" position="45,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_Temperature1" font="Prive3;37" position="157,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_state1" font="Prive3;33" position="7,303" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="black" transparent="1" />
<widget name="Weather_Date1" font="Prive3;33" position="7,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="black" transparent="1" />

<widget name="Weather_picon2" pixmap="hd_glass17/icons/3200.png" position="412,382" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow2" font="Prive3;36" position="352,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_Temperature2" font="Prive3;37" position="465,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_state2" font="Prive3;33" position="315,303" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="black" transparent="1" />
<widget name="Weather_Date2" font="Prive3;33" position="315,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="black" transparent="1" />

<widget name="Weather_picon3" pixmap="hd_glass17/icons/3200.png" position="720,382" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow3" font="Prive3;36" position="660,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_Temperature3" font="Prive3;37" position="772,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_state3" font="Prive3;33" position="622,303" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="black" transparent="1" />
<widget name="Weather_Date3" font="Prive3;33" position="622,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="black" transparent="1" />

<widget name="Weather_picon4" pixmap="hd_glass17/icons/3200.png" position="1027,382" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow4" font="Prive3;36" position="967,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_Temperature4" font="Prive3;37" position="1080,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_state4" font="Prive3;33" position="930,303" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="black" transparent="1" />
<widget name="Weather_Date4" font="Prive3;33" position="930,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="black" transparent="1" />

<widget name="Weather_picon5" pixmap="hd_glass17/icons/3200.png" position="1335,382" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow5" font="Prive3;36" position="1275,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_Temperature5" font="Prive3;37" position="1387,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_state5" font="Prive3;33" position="1237,303" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="black" transparent="1" />
<widget name="Weather_Date5" font="Prive3;33" position="1237,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="black" transparent="1" />

<widget name="moon_pict" position="1010,29" zPosition="5" size="0,0" alphatest="blend" />
<widget name="moon_phase" font="Prive3;24" position="952,176" zPosition="3" size="0,0" valign="top" halign="center" foregroundColor="#00d100" backgroundColor="background" transparent="1" />

</screen>"""

skinWea["7"] = """<screen name="WeatherScreen" position="645,163" size="1177,487" title="Weather" zPosition="8" backgroundColor="background" >                                           

<widget name="Weather_items" font="Prive3;23" position="0,15" zPosition="2" size="197,300" valign="top" halign="right" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_values" font="Prive3;23" position="212,15" zPosition="3" size="280,300" valign="top" halign="left"  backgroundColor="background" transparent="1" />

<widget name="Weather_picon0" pixmap="hd_glass17/icons/3200.png" position="422,52" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperature0" font="Prive3;31" position="364,168" zPosition="2" size="225,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state0" font="Prive3;24" position="364,0" zPosition="3" size="225,52" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<eLabel position="7,213" zPosition="8" size="1162,1" backgroundColor="#1546AF" transparent="0" />

<widget name="Weather_wind" pixmap="hd_glass17/icons/no-wind.png" position="582,25" zPosition="5" size="150,150" alphatest="blend" />
<widget name="Weather_wind_label" font="Prive3;27" position="608,7" zPosition="2" size="0,0" valign="center" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_sunrise" font="Prive3;24" position="737,78" zPosition="5" size="225,30" valign="top" halign="center" foregroundColor="#ffcc00" backgroundColor="background" transparent="1" />
<widget name="Weather_sunset" font="Prive3;24" position="737,186" zPosition="5" size="225,30" valign="top" halign="center" foregroundColor="#ff3300" backgroundColor="background" transparent="1" />
<ePixmap position="775,0" zPosition="6" size="148,75" pixmap="hd_glass17/icons/Sunrise-fs8.png" alphatest="blend"/>
<ePixmap position="775,108" zPosition="6" size="148,75" pixmap="hd_glass17/icons/Sunset-fs8.png" alphatest="blend"/>

<widget name="moon_pict" position="1010,15" zPosition="5" size="108,108" alphatest="blend" />
<widget name="moon_phase" font="Prive3;24" position="952,150" zPosition="3" size="225,52" valign="top" halign="center" foregroundColor="#00d100" backgroundColor="background" transparent="1" />

<widget name="Weather_picon1" pixmap="hd_glass17/icons/3200.png" position="67,277" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow1" font="Prive3;31" position="22,390" zPosition="2" size="97,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature1" font="Prive3;31" position="120,390" zPosition="2" size="97,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state1" font="Prive3;24" position="7,225" zPosition="3" size="225,52" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date1" font="Prive3;24" position="7,427" zPosition="3" size="225,52" valign="top" halign="center"  foregroundColor="#CC3399" backgroundColor="background" transparent="1" />

<widget name="Weather_picon2" pixmap="hd_glass17/icons/3200.png" position="300,277" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow2" font="Prive3;31" position="255,390" zPosition="2" size="97,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature2" font="Prive3;31" position="352,390" zPosition="2" size="97,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state2" font="Prive3;24" position="240,225" zPosition="3" size="225,52" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date2" font="Prive3;24" position="240,427" zPosition="3" size="225,52" valign="top" halign="center"  foregroundColor="#CC3399" backgroundColor="background" transparent="1" />

<widget name="Weather_picon3" pixmap="hd_glass17/icons/3200.png" position="532,277" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow3" font="Prive3;31" position="487,390" zPosition="2" size="97,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature3" font="Prive3;31" position="585,390" zPosition="2" size="97,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state3" font="Prive3;24" position="472,225" zPosition="3" size="225,52" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date3" font="Prive3;24" position="472,427" zPosition="3" size="225,52" valign="top" halign="center"  foregroundColor="#CC3399" backgroundColor="background" transparent="1" />

<widget name="Weather_picon4" pixmap="hd_glass17/icons/3200.png" position="765,277" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow4" font="Prive3;31" position="720,390" zPosition="2" size="97,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature4" font="Prive3;31" position="817,390" zPosition="2" size="97,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state4" font="Prive3;24" position="705,225" zPosition="3" size="225,52" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date4" font="Prive3;24" position="705,427" zPosition="3" size="225,52" valign="top" halign="center"  foregroundColor="#CC3399" backgroundColor="background" transparent="1" />

<widget name="Weather_picon5" pixmap="hd_glass17/icons/3200.png" position="997,277" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow5" font="Prive3;31" position="952,390" zPosition="2" size="97,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature5" font="Prive3;31" position="1050,390" zPosition="2" size="97,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state5" font="Prive3;24" position="937,225" zPosition="3" size="225,52" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date5" font="Prive3;24" position="937,427" zPosition="3" size="225,52" valign="top" halign="center"  foregroundColor="#CC3399" backgroundColor="background" transparent="1" />

</screen>"""

skinWea["8"] = """<screen name="WeatherScreen" position="832,150" size="990,502" zPosition="8" title="Weather" backgroundColor="background" >                                           
<widget name="Weather_sunrise" font="Prive3;33" position="1275,237" zPosition="5" size="0,0" valign="top" halign="center" foregroundColor="#66CCFF" backgroundColor="background" transparent="1" />
<widget name="Weather_wind" pixmap="hd_glass17/icons/no-wind.png" position="975,60" zPosition="5" size="0,0" alphatest="blend" />
<widget name="Weather_wind_label" font="Prive3;33" position="855,7" zPosition="2" size="0,0" valign="center" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_picon1" pixmap="hd_glass17/icons/3200.png" position="105,382" zPosition="5" size="0,0" alphatest="blend" />
<widget name="Weather_state1" font="Prive3;33" position="7,303" zPosition="3" size="0,0" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date1" font="Prive3;33" position="7,540" zPosition="3" size="0,0" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_sunset" font="Prive3;33" position="15,0" zPosition="2" size="310,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature0" font="Prive3;60" position="30,60" zPosition="2" size="150,67" valign="top" halign="left" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_picon0" pixmap="hd_glass17/icons/3200.png" position="195,45" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_state0" font="Prive3;25" position="15,157" zPosition="3" size="300,52" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<eLabel text="Max:" font="Prive3;27" position="22,210" zPosition="2" size="75,60" valign="top" halign="left" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature1" font="Prive3;27" position="105,210" zPosition="2" size="105,60" valign="top" halign="left" foregroundColor="red" backgroundColor="background" transparent="1" />
<eLabel text="Min:" font="Prive3;27" position="195,210" zPosition="2" size="75,60" valign="top" halign="left" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperaturelow1" font="Prive3;27" position="277,210" zPosition="2" size="112,60" valign="top" halign="left" foregroundColor="blue" backgroundColor="background" transparent="1" />

<widget name="moon_pict" position="400,29" zPosition="5" size="108,108" alphatest="blend" />
<widget name="moon_phase" font="Prive3;25" position="342,157" zPosition="3" size="225,52" valign="center" halign="center" foregroundColor="#00d100" backgroundColor="background" transparent="1" />

<widget name="Weather_items" font="Prive3;25" position="445,7" zPosition="2" size="310,345" valign="top" halign="right" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_values" font="Prive3;25" position="770,7" zPosition="3" size="450,345" valign="top" halign="left"  backgroundColor="background" transparent="1" />
<eLabel position="7,262" zPosition="8" size="1530,1" backgroundColor="#1546AF" transparent="0" />

<widget name="Weather_state2" font="Prive3;25" position="15,270" zPosition="3" size="300,52" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_picon2" pixmap="hd_glass17/icons/3200.png" position="15,325" zPosition="5" size="108,108" alphatest="blend" />
<ePixmap position="135,348" zPosition="7" size="28,24" pixmap="hd_glass17/icons/up.png" alphatest="on"/>
<widget name="Weather_Temperature2" font="Prive3;31" position="172,337" zPosition="2" size="112,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<ePixmap position="135,390" zPosition="7" size="28,24" pixmap="hd_glass17/icons/down.png" alphatest="on"/>
<widget name="Weather_Temperaturelow2" font="Prive3;31" position="172,379" zPosition="2" size="112,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Date2" font="Prive3;25" position="15,441" zPosition="3" size="300,52" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_state3" font="Prive3;25" position="352,270" zPosition="3" size="300,52" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_picon3" pixmap="hd_glass17/icons/3200.png" position="352,325" zPosition="5" size="108,108" alphatest="blend" />
<ePixmap position="472,348" zPosition="7" size="28,24" pixmap="hd_glass17/icons/up.png" alphatest="on"/>
<widget name="Weather_Temperature3" font="Prive3;31" position="510,337" zPosition="2" size="112,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<ePixmap position="472,390" zPosition="7" size="28,24" pixmap="hd_glass17/icons/down.png" alphatest="on"/>
<widget name="Weather_Temperaturelow3" font="Prive3;31" position="510,379" zPosition="2" size="112,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Date3" font="Prive3;25" position="352,441" zPosition="3" size="300,52" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_state4" font="Prive3;25" position="675,270" zPosition="3" size="300,52" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_picon4" pixmap="hd_glass17/icons/3200.png" position="675,325" zPosition="5" size="108,108" alphatest="blend" />
<ePixmap position="795,348" zPosition="7" size="28,24" pixmap="hd_glass17/icons/up.png" alphatest="on"/>
<widget name="Weather_Temperature4" font="Prive3;31" position="832,337" zPosition="2" size="112,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<ePixmap position="795,390" zPosition="7" size="28,24" pixmap="hd_glass17/icons/down.png" alphatest="on"/>
<widget name="Weather_Temperaturelow4" font="Prive3;31" position="832,379" zPosition="2" size="112,37" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Date4" font="Prive3;25" position="675,441" zPosition="3" size="300,52" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_picon5" pixmap="hd_glass17/icons/3200.png" position="997,277" zPosition="5" size="0,0" alphatest="blend" />
<widget name="Weather_Temperaturelow5" font="Prive3;31" position="952,390" zPosition="2" size="0,0" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature5" font="Prive3;31" position="1050,390" zPosition="2" size="0,0" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state5" font="Prive3;24" position="937,225" zPosition="3" size="0,0" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date5" font="Prive3;24" position="937,427" zPosition="3" size="0,0" valign="top" halign="center"  foregroundColor="#CC3399" backgroundColor="background" transparent="1" />

</screen>"""

skinWea["9"] = """<screen name="WeatherScreen" position="center,120" size="1545,645" zPosition="8" title="Weather" backgroundColor="background" >                                           

<widget name="Weather_items" font="Prive3;30" position="0,25" zPosition="2" size="280,300" valign="top" halign="right" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_values" font="Prive3;30" position="295,25" zPosition="3" size="400,300" valign="top" halign="left"  backgroundColor="background" transparent="1" />

<widget name="Weather_picon0" pixmap="hd_glass17/icons/3200.png" position="630,90" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperature0" font="Prive3;37" position="532,217" zPosition="2" size="300,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state0" font="Prive3;33" position="532,7" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<eLabel position="7,289" zPosition="8" size="1530,1" backgroundColor="#1546AF" transparent="0" />

<widget name="Weather_wind" pixmap="hd_glass17/icons/no-wind.png" position="875,95" zPosition="5" size="158,158" alphatest="blend" />
<widget name="Weather_wind_label" font="Prive3;33" position="740,7" zPosition="2" size="430,75" valign="center" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_sunrise" font="Prive3;33" position="1080,102" zPosition="5" size="225,37" valign="top" halign="center" foregroundColor="#ffcc00" backgroundColor="background" transparent="1" />
<widget name="Weather_sunset" font="Prive3;33" position="1080,237" zPosition="5" size="225,37" valign="top" halign="center" foregroundColor="#ff3300" backgroundColor="background" transparent="1" />
<ePixmap position="1117,15" zPosition="6" size="148,75" pixmap="hd_glass17/icons/Sunrise-fs8.png" alphatest="blend"/>
<ePixmap position="1117,150" zPosition="6" size="148,75" pixmap="hd_glass17/icons/Sunset-fs8.png" alphatest="blend"/>

<widget name="moon_pict" position="1348,100" zPosition="5" size="158,158" alphatest="blend" />
<widget name="moon_phase" font="Prive3;33" position="1315,7" zPosition="3" size="225,75" valign="center" halign="center" foregroundColor="#00d100" backgroundColor="background" transparent="1" />

<widget name="Weather_picon1" pixmap="hd_glass17/icons/3200.png" position="105,382" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow1" font="Prive3;36" position="45,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature1" font="Prive3;37" position="157,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state1" font="Prive3;33" position="7,303" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date1" font="Prive3;33" position="7,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_picon2" pixmap="hd_glass17/icons/3200.png" position="412,382" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow2" font="Prive3;36" position="352,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature2" font="Prive3;37" position="465,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state2" font="Prive3;33" position="315,303" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date2" font="Prive3;33" position="315,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_picon3" pixmap="hd_glass17/icons/3200.png" position="720,382" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow3" font="Prive3;36" position="660,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature3" font="Prive3;37" position="772,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state3" font="Prive3;33" position="622,303" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date3" font="Prive3;33" position="622,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_picon4" pixmap="hd_glass17/icons/3200.png" position="1027,382" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow4" font="Prive3;36" position="967,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature4" font="Prive3;37" position="1080,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state4" font="Prive3;33" position="930,303" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date4" font="Prive3;33" position="930,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_picon5" pixmap="hd_glass17/icons/3200.png" position="1335,382" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow5" font="Prive3;36" position="1275,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature5" font="Prive3;37" position="1387,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state5" font="Prive3;33" position="1237,303" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date5" font="Prive3;33" position="1237,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

</screen>"""

skinWea["10"] = """<screen name="WeatherScreen" position="center,120" size="1300,645" zPosition="8" title="Weather" backgroundColor="background" >                                           
<widget name="Weather_sunrise" font="Prive3;33" position="1275,237" zPosition="5" size="0,0" valign="top" halign="center" foregroundColor="#66CCFF" backgroundColor="background" transparent="1" />
<widget name="Weather_wind" pixmap="hd_glass17/icons/no-wind.png" position="975,60" zPosition="5" size="0,0" alphatest="blend" />
<widget name="Weather_wind_label" font="Prive3;33" position="855,7" zPosition="2" size="0,0" valign="center" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_picon1" pixmap="hd_glass17/icons/3200.png" position="105,382" zPosition="5" size="0,0" alphatest="blend" />
<widget name="Weather_state1" font="Prive3;33" position="7,303" zPosition="3" size="0,0" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date1" font="Prive3;33" position="7,540" zPosition="3" size="0,0" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_sunset" font="Prive3;37" position="15,15" zPosition="2" size="310,45" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature0" font="Prive3;75" position="15,67" zPosition="2" size="150,90" valign="top" halign="left" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_picon0" pixmap="hd_glass17/icons/3200.png" position="195,67" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_state0" font="Prive3;33" position="15,180" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<eLabel text="Max:" font="Prive3;30" position="15,255" zPosition="2" size="75,60" valign="top" halign="left" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature1" font="Prive3;30" position="105,255" zPosition="2" size="105,60" valign="top" halign="left" foregroundColor="red" backgroundColor="background" transparent="1" />
<eLabel text="Min:" font="Prive3;30" position="195,255" zPosition="2" size="75,60" valign="top" halign="left" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperaturelow1" font="Prive3;30" position="285,255" zPosition="2" size="112,60" valign="top" halign="left" foregroundColor="blue" backgroundColor="background" transparent="1" />

<widget name="Weather_items" font="Prive3;30" position="375,7" zPosition="2" size="310,345" valign="top" halign="right" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_values" font="Prive3;30" position="700,7" zPosition="3" size="450,345" valign="top" halign="left"  backgroundColor="background" transparent="1" />
<eLabel position="7,322" zPosition="8" size="1530,1" backgroundColor="#1546AF" transparent="0" />

<widget name="moon_pict" position="1097,29" zPosition="5" size="108,108" alphatest="blend" />
<widget name="moon_phase" font="Prive3;33" position="1002,180" zPosition="3" size="300,75" valign="center" halign="center" foregroundColor="#00d100" backgroundColor="background" transparent="1" />

<widget name="Weather_state2" font="Prive3;33" position="15,345" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_picon2" pixmap="hd_glass17/icons/3200.png" position="15,424" zPosition="5" size="108,108" alphatest="blend" />
<ePixmap position="135,435" zPosition="7" size="28,24" pixmap="hd_glass17/icons/up.png" alphatest="on"/>
<widget name="Weather_Temperature2" font="Prive3;37" position="172,424" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<ePixmap position="135,487" zPosition="7" size="28,24" pixmap="hd_glass17/icons/down.png" alphatest="on"/>
<widget name="Weather_Temperaturelow2" font="Prive3;36" position="172,477" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Date2" font="Prive3;33" position="15,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_state3" font="Prive3;33" position="502,345" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_picon3" pixmap="hd_glass17/icons/3200.png" position="502,424" zPosition="5" size="108,108" alphatest="blend" />
<ePixmap position="622,435" zPosition="7" size="28,24" pixmap="hd_glass17/icons/up.png" alphatest="on"/>
<widget name="Weather_Temperature3" font="Prive3;37" position="660,424" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<ePixmap position="622,487" zPosition="7" size="28,24" pixmap="hd_glass17/icons/down.png" alphatest="on"/>
<widget name="Weather_Temperaturelow3" font="Prive3;36" position="660,477" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Date3" font="Prive3;33" position="502,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_state4" font="Prive3;33" position="975,345" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_picon4" pixmap="hd_glass17/icons/3200.png" position="975,424" zPosition="5" size="108,108" alphatest="blend" />
<ePixmap position="1095,435" zPosition="7" size="28,24" pixmap="hd_glass17/icons/up.png" alphatest="on"/>
<widget name="Weather_Temperature4" font="Prive3;37" position="1132,424" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<ePixmap position="1095,487" zPosition="7" size="28,24" pixmap="hd_glass17/icons/down.png" alphatest="on"/>
<widget name="Weather_Temperaturelow4" font="Prive3;36" position="1132,477" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Date4" font="Prive3;33" position="975,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

<widget name="Weather_picon5" pixmap="hd_glass17/icons/3200.png" position="1535,382" zPosition="5" size="0,0" alphatest="blend" />
<widget name="Weather_Temperaturelow5" font="Prive3;36" position="1475,495" zPosition="2" size="0,0" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature5" font="Prive3;37" position="1587,495" zPosition="2" size="0,0" valign="top" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_state5" font="Prive3;33" position="1437,303" zPosition="3" size="0,0" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date5" font="Prive3;33" position="1437,540" zPosition="3" size="0,0" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="background" transparent="1" />

</screen>"""

skinWea["11"] = """<screen name="WeatherScreen" position="0,0" size="1920,1080" zPosition="8" title="Weather" backgroundColor="black" flags="wfNoBorder" >                                                                                              
<widget source="Title" render="Label" position="174,96" size="1570,49" zPosition="1" font="Prive3;37" halign="center" transparent="1" foregroundColor="#00ff8000" shadowColor="#1A58A6" shadowOffset="-2,-1" />
<widget name="Weather_items" font="Prive3;30" position="54,225" zPosition="2" size="315,300" valign="top" halign="right" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_values" font="Prive3;30" position="384,225" zPosition="3" size="315,300" valign="top" halign="left"  backgroundColor="background" transparent="1" />

<widget name="Weather_picon0" pixmap="hd_glass17/icons/3200.png" position="702,270" zPosition="1" size="192,192" transparent="1" alphatest="blend" />
<widget name="Weather_Temperature0" font="Regular;34" position="702,477" zPosition="3" size="192,60" valign="center" halign="center" foregroundColor="#cc3300" backgroundColor="background" transparent="1" />
<widget name="Weather_state0" font="Prive3;30" position="648,165" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_wind" position="1335,293" zPosition="5" size="158,158" alphatest="blend" />
<widget name="Weather_wind_label" font="Prive3;30" position="1215,165" zPosition="2" size="400,84" valign="center" halign="center" foregroundColor="yellow" backgroundColor="background" transparent="1" />
<widget name="Weather_sunrise" font="Prive3;30" position="985,165" zPosition="5" size="150,84" valign="center" halign="center" foregroundColor="#ffcc00" backgroundColor="background" transparent="1" />
<widget name="Weather_sunset" font="Prive3;30" position="1135,165" zPosition="5" size="150,84" valign="center" halign="center" foregroundColor="#ff3300" backgroundColor="background" transparent="1" />
<ePixmap position="985,366" zPosition="6" size="148,75" pixmap="hd_glass17/icons/Sunrise-fs8.png" alphatest="blend"/>
<ePixmap position="1135,366" zPosition="6" size="148,75" pixmap="hd_glass17/icons/Sunset-fs8.png" alphatest="blend"/>

<widget name="moon_pict" position="1572,295" zPosition="5" size="158,158" alphatest="blend" />
<widget name="moon_phase" font="Prive3;30" position="1527,165" zPosition="3" size="250,75" valign="center" halign="center" foregroundColor="#00d100" backgroundColor="background" transparent="1" />

<widget name="Weather_picon1" pixmap="hd_glass17/icons/3200.png" position="208,630" zPosition="1" size="192,192" transparent="1" alphatest="blend" backgroundColor="background" />
<widget name="Weather_Temperaturelow1" font="Regular;34" position="208,832" zPosition="2" size="96,60" valign="center" halign="center" foregroundColor="blue" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature1" font="Regular;34" position="304,832" zPosition="2" size="96,60" valign="center" halign="center" foregroundColor="#cc3300" backgroundColor="background" transparent="1" />
<widget name="Weather_state1" font="Prive3;30" position="154,540" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date1" font="Prive3;30" position="154,897" zPosition="3" size="300,66" valign="top" halign="center"  foregroundColor="#26cfc0" backgroundColor="background" transparent="1" />

<widget name="Weather_picon2" pixmap="hd_glass17/icons/3200.png" position="535,630" zPosition="1" size="192,192" transparent="1" alphatest="blend" />
<widget name="Weather_Temperaturelow2" font="Regular;34" position="535,832" zPosition="2" size="96,60" valign="center" halign="center" foregroundColor="blue" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature2" font="Regular;34" position="631,832" zPosition="2" size="96,60" valign="center" halign="center" foregroundColor="#cc3300" backgroundColor="background" transparent="1" />
<widget name="Weather_state2" font="Prive3;30" position="481,540" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date2" font="Prive3;30" position="481,897" zPosition="3" size="300,66" valign="top" halign="center"  foregroundColor="#26cfc0" backgroundColor="background" transparent="1" />

<widget name="Weather_picon3" pixmap="hd_glass17/icons/3200.png" position="862,630" zPosition="1" size="192,192" transparent="1" alphatest="blend" />
<widget name="Weather_Temperaturelow3" font="Regular;34" position="862,832" zPosition="2" size="96,60" valign="center" halign="center" foregroundColor="blue" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature3" font="Regular;34" position="958,832" zPosition="2" size="96,60" valign="center" halign="center" foregroundColor="#cc3300" backgroundColor="background" transparent="1" />
<widget name="Weather_state3" font="Prive3;30" position="808,540" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date3" font="Prive3;30" position="808,897" zPosition="3" size="300,66" valign="top" halign="center"  foregroundColor="#26cfc0" backgroundColor="background" transparent="1" />

<widget name="Weather_picon4" pixmap="hd_glass17/icons/3200.png" position="1189,630" zPosition="1" size="192,192" transparent="1" alphatest="blend" />
<widget name="Weather_Temperaturelow4" font="Regular;34" position="1189,832" zPosition="2" size="96,60" valign="center" halign="center" foregroundColor="blue" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature4" font="Regular;34" position="1285,832" zPosition="2" size="96,60" valign="center" halign="center" foregroundColor="#cc3300" backgroundColor="background" transparent="1" />
<widget name="Weather_state4" font="Prive3;30" position="1135,540" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date4" font="Prive3;30" position="1135,897" zPosition="3" size="300,66" valign="top" halign="center"  foregroundColor="#26cfc0" backgroundColor="background" transparent="1" />

<widget name="Weather_picon5" pixmap="hd_glass17/icons/3200.png" position="1516,630" zPosition="1" size="192,192" transparent="1" alphatest="blend" />
<widget name="Weather_Temperaturelow5" font="Regular;34" position="1516,832" zPosition="2" size="96,60" valign="center" halign="center" foregroundColor="blue" backgroundColor="background" transparent="1" />
<widget name="Weather_Temperature5" font="Regular;34" position="1612,832" zPosition="2" size="96,60" valign="center" halign="center" foregroundColor="#cc3300" backgroundColor="background" transparent="1" />
<widget name="Weather_state5" font="Prive3;30" position="1462,540" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="background" transparent="1" />
<widget name="Weather_Date5" font="Prive3;30" position="1462,897" zPosition="3" size="300,66" valign="top" halign="center"  foregroundColor="#26cfc0" backgroundColor="background" transparent="1" />

</screen>"""

skinWea["12"] = """<screen name="WeatherScreen" position="center,120" size="1545,645" zPosition="8" title="Weather" backgroundColor="black" >                                           
<widget name="Weather_items" font="Prive3;30" position="0,25" zPosition="2" size="280,300" valign="top" halign="right" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_values" font="Prive3;30" position="295,25" zPosition="3" size="400,300" valign="top" halign="left"  backgroundColor="black" transparent="1" />

<widget name="Weather_picon0" pixmap="hd_glass17/icons/3200.png" position="630,90" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperature0" font="Prive3;65" position="532,207" zPosition="2" size="300,70" valign="top" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_state0" font="Prive3;33" position="532,7" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="black" transparent="1" />
<eLabel position="7,289" zPosition="8" size="1530,1" backgroundColor="#1546AF" transparent="0" />

<widget name="Weather_wind" pixmap="hd_glass17/icons/no-wind.png" position="875,95" zPosition="5" size="158,158" alphatest="blend" />
<widget name="Weather_wind_label" font="Prive3;33" position="740,7" zPosition="2" size="430,75" valign="center" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_sunrise" font="Prive3;33" position="1080,102" zPosition="5" size="225,37" valign="top" halign="center" foregroundColor="#ffcc00" backgroundColor="black" transparent="1" />
<widget name="Weather_sunset" font="Prive3;33" position="1080,237" zPosition="5" size="225,37" valign="top" halign="center" foregroundColor="#ff3300" backgroundColor="black" transparent="1" />
<ePixmap position="1117,15" zPosition="6" size="148,75" pixmap="hd_glass17/icons/Sunrise-fs8.png" alphatest="blend"/>
<ePixmap position="1117,150" zPosition="6" size="148,75" pixmap="hd_glass17/icons/Sunset-fs8.png" alphatest="blend"/>

<widget name="moon_pict" position="1348,100" zPosition="5" size="158,158" alphatest="blend" />
<widget name="moon_phase" font="Prive3;33" position="1315,7" zPosition="3" size="225,75" valign="center" halign="center" foregroundColor="#00d100" backgroundColor="black" transparent="1" />

<widget name="Weather_picon1" pixmap="hd_glass17/icons/3200.png" position="105,382" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow1" font="Prive3;36" position="45,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_Temperature1" font="Prive3;37" position="157,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_state1" font="Prive3;33" position="7,303" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="black" transparent="1" />
<widget name="Weather_Date1" font="Prive3;33" position="7,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="black" transparent="1" />

<widget name="Weather_picon2" pixmap="hd_glass17/icons/3200.png" position="412,382" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow2" font="Prive3;36" position="352,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_Temperature2" font="Prive3;37" position="465,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_state2" font="Prive3;33" position="315,303" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="black" transparent="1" />
<widget name="Weather_Date2" font="Prive3;33" position="315,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="black" transparent="1" />

<widget name="Weather_picon3" pixmap="hd_glass17/icons/3200.png" position="720,382" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow3" font="Prive3;36" position="660,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_Temperature3" font="Prive3;37" position="772,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_state3" font="Prive3;33" position="622,303" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="black" transparent="1" />
<widget name="Weather_Date3" font="Prive3;33" position="622,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="black" transparent="1" />

<widget name="Weather_picon4" pixmap="hd_glass17/icons/3200.png" position="1027,382" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow4" font="Prive3;36" position="967,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_Temperature4" font="Prive3;37" position="1080,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_state4" font="Prive3;33" position="930,303" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="black" transparent="1" />
<widget name="Weather_Date4" font="Prive3;33" position="930,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="black" transparent="1" />

<widget name="Weather_picon5" pixmap="hd_glass17/icons/3200.png" position="1335,382" zPosition="5" size="108,108" alphatest="blend" />
<widget name="Weather_Temperaturelow5" font="Prive3;36" position="1275,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_Temperature5" font="Prive3;37" position="1387,495" zPosition="2" size="112,60" valign="top" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
<widget name="Weather_state5" font="Prive3;33" position="1237,303" zPosition="3" size="300,75" valign="center" halign="center"  foregroundColor="#00d100" backgroundColor="black" transparent="1" />
<widget name="Weather_Date5" font="Prive3;33" position="1237,540" zPosition="3" size="300,75" valign="top" halign="center"  foregroundColor="#EF3399" backgroundColor="black" transparent="1" />

</screen>"""
