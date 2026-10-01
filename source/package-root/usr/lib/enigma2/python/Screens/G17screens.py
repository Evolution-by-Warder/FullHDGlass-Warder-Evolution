from Components.config import config
PATH = "%s/extraScreens17" % config.plugins.setupGlass17.par39.value
g17_extraScreen = {}
g17_extraScreen["1"] = """
                                             
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="hd_glass17/general/infobar-ex.png" alphatest="off" />

    <widget source="session.CurrentService" render="Label" position="285,765" size="120,39" font="Prive4;33" halign="right" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2" valign="bottom">
      <convert type="g17ServiceNum">Number</convert>
    </widget>
    <widget position="435,757" size="757,48" source="session.CurrentService" render="Label" font="Prive4;39" valign="bottom" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="ServiceName">Name</convert>
    </widget>
    <ePixmap position="120,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="960,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <widget name="TP_info" position="318,951" zPosition="2" size="750,30" font="Prive4;24" halign="left" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />
    <widget name="TP_type" position="121,952" zPosition="1" size="293,30" font="Prive4;22" halign="left" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />
    <widget name="Video_size" font="Prive4;27" position="115,766" size="180,33" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1609,754" size="135,48" font="Prive4;39" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1725,757" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="937,766" size="660,33" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="1075,826" size="525,37" font="Prive4;27" halign="right" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

    <widget name="Dtype" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
        
    <ePixmap position="111,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="130,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />

    <widget position="315,858" size="90,39" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,858" size="495,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,858" size="142,39" source="session.Event_Now" render="Label" zPosition="1" backgroundColor="background" transparent="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="313,837" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="313,837" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="blend" />
    <widget position="315,892" size="90,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,892" size="495,39" source="session.Event_Next" render="g17EmptyEpg" backgroundColor="background" transparent="1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,892" size="142,39" source="session.Event_Next" render="Label" backgroundColor="background" transparent="1" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    <ePixmap position="1620,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />          
    <widget name="picProvSat" position="1639,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />
    <widget name="weaTxt" position="1639,835" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />

    <widget name="subserv" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1569,871" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1569,871" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1569,871" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>    
    <widget name="ecmLineInfo" position="780,994" size="1017,24" font="Prive4;18" noWrap="1" halign="right" transparent="1" backgroundColor="background" foregroundColor="unb2e0b4" zPosition="5" />
    <eLabel text="Snr: dB" font="Prive4;24" position="121,988" size="105,30" foregroundColor="un99bad6" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="226,988" size="90,30" font="Prive4;24" transparent="1" backgroundColor="background" zPosition="5" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">SnrdB</convert>
    </widget>
    <eLabel text="Snr:" position="319,988" size="60,30" font="Prive4;24" foregroundColor="un99bad6" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="379,988" size="90,30" transparent="1" backgroundColor="background" font="Prive4;24" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="469,988" size="60,30" font="Prive4;24" foregroundColor="un99bad6" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="529,988" size="90,30" transparent="1" backgroundColor="background" font="Prive4;24" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <eLabel text="Ber:" position="619,988" size="60,30" font="Prive4;24" foregroundColor="un99bad6" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="679,988" size="90,30" transparent="1" backgroundColor="background" font="Prive4;24" foregroundColor="unefb2b2">
      <convert type="g17ExtraSource">BerText</convert>
    </widget>
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="caidPids" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" transparent="1" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    
  </screen>"""
  
g17_extraScreen["2"] = """

  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""

g17_extraScreen["2"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/2/infobar-ext3.png" alphatest="off"/>\n'
g17_extraScreen["2"]  += """<widget source="session.CurrentService" render="Label" position="322,762" size="120,52"  font="Prive3;42" halign="left" transparent="1" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2">	
    <convert type="g17ServiceNum">Number</convert>
    </widget>
    
    <widget position="442,762" size="757,52" source="session.CurrentService" render="Label" font="Prive3;42" valign="bottom" halign="left" noWrap="1" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
			<convert type="ServiceName">Name</convert>
		</widget>

		<ePixmap position="120,952" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png"/>
		<ePixmap position="960,952" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png"/>

    <widget name="TP_info" position="300,970" zPosition="1" size="783,34" font="Prive3;27" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>
    <widget name="TP_type" position="67,970" zPosition="1" size="279,34" font="Prive3;27" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>

		<widget name="Video_size"	font="Prive3;27" position="120,775" size="166,34" halign="center"  backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>

		<widget source="global.CurrentTime" 	render="Label" position="1611,762" size="135,52" font="Prive3;42" valign="top" halign="right" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
			<convert type="g17ClockToText">Default</convert>
		</widget>
		<widget source="global.CurrentTime" 	render="Label" position="1738,765" size="52,30" font="Prive3;30" valign="top" halign="right" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
			<convert type="g17ClockToText">Format::%S</convert>
		</widget>
		<widget source="global.CurrentTime" render="g17dateFormat" format="%A, %d %B %Y" position="945,775" size="660,30" font="Prive3;27" halign="right" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="1275,828" size="525,33" font="Prive3;27" transparent="1" halign="right" backgroundColor="background" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="Dcam" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="Decm" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm"	pixmap="hd_glass17/icons/irdemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D2_Demm"	pixmap="hd_glass17/icons/secemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D3_Demm"	pixmap="hd_glass17/icons/nagemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D4_Demm"	pixmap="hd_glass17/icons/viaemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D5_Demm"	pixmap="hd_glass17/icons/conemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D0_Demm"	pixmap="hd_glass17/icons/betemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D6_Demm"	pixmap="hd_glass17/icons/crwemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D7_Demm"	pixmap="hd_glass17/icons/drcemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
           
    <ePixmap position="105,825" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />    
    <widget name="g17picon" position="124,841" size="150,90" zPosition="2" transparent="1" alphatest="on" />    	

		<widget position="322,859" size="97,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
			<convert type="g17EventTime">StartTime</convert>
		</widget>
		<widget position="442,861" size="466,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive3;30" valign="bottom" noWrap="1" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
			<convert type="EventName">Name</convert>
		</widget>
		<widget position="916,859" size="142,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="right" transparent="1">
			<convert type="g17EventTime">Remaining</convert>
		</widget>
		
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="321,829" size="762,21" zPosition="3" transparent="1" >
			<convert type="EventTime">Progress</convert>
		</widget>
    <widget name="slider_back" position="321,829" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />		
		<widget position="322,898" size="97,39" source="session.Event_Next" render="Label" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
			<convert type="g17EventTime">StartTime</convert>
		</widget>
		<widget position="442,900" size="466,39" source="session.Event_Next" render="g17EmptyEpg" font="Prive3;30" valign="bottom" noWrap="1" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
			<convert type="EventName">Name</convert>
		</widget>
		<widget position="916,898" size="142,39" source="session.Event_Next" render="Label" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" halign="right" transparent="1">
			<convert type="g17EventTime">Duration</convert>
		</widget>

    <widget name="subserv" position="1771,874" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1771,874" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
  	<widget name="dolby" position="1771,874" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
  	<widget name="txt" position="1771,874" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
		<widget name="tuner" position="1771,874" size="42,72" zPosition="1" alphatest="off"/>
    <widget name="HDD_state" position="1771,874" size="42,72" zPosition="1" alphatest="off" />    
		<widget position="1771,874" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on" >
			<convert type="g17ConditionalShowHide">Blink</convert>
		</widget> 
		
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="caidPids" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" transparent="1" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" transparent="1" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />

	</screen>""" 
	
g17_extraScreen["3"] = """

  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""
g17_extraScreen["3"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/3/infobar-ext3.png" alphatest="off"/>\n'
g17_extraScreen["3"]  += """<widget source="session.CurrentService" render="Label" position="322,762" size="120,52"  font="Prive3;42" halign="left" transparent="1" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2">	
    <convert type="g17ServiceNum">Number</convert>
    </widget>
    
    <widget position="442,762" size="757,52" source="session.CurrentService" render="Label" font="Prive3;42" valign="bottom" halign="left" noWrap="1" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
			<convert type="ServiceName">Name</convert>
		</widget>

		<ePixmap position="120,952" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png"/>
		<ePixmap position="960,952" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png"/>

    <widget name="TP_info" position="300,970" zPosition="1" size="783,34" font="Prive3;27" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>
    <widget name="TP_type" position="67,970" zPosition="1" size="279,34" font="Prive3;27" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>

		<widget name="Video_size"	font="Prive3;27" position="120,775" size="166,34" halign="center"  backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>

		<widget source="global.CurrentTime" 	render="Label" position="1611,762" size="135,52" font="Prive3;42" valign="top" halign="right" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
			<convert type="g17ClockToText">Default</convert>
		</widget>
		<widget source="global.CurrentTime" 	render="Label" position="1738,765" size="52,30" font="Prive3;30" valign="top" halign="right" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
			<convert type="g17ClockToText">Format::%S</convert>
		</widget>
		<widget source="global.CurrentTime" render="g17dateFormat" format="%A, %d %B %Y" position="945,775" size="660,30" font="Prive3;27" halign="right" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="1083,828" size="525,33" font="Prive3;27" halign="right" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="Dcam" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="Decm" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm"	pixmap="hd_glass17/icons/irdemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D2_Demm"	pixmap="hd_glass17/icons/secemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D3_Demm"	pixmap="hd_glass17/icons/nagemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D4_Demm"	pixmap="hd_glass17/icons/viaemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D5_Demm"	pixmap="hd_glass17/icons/conemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D0_Demm"	pixmap="hd_glass17/icons/betemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D6_Demm"	pixmap="hd_glass17/icons/crwemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D7_Demm"	pixmap="hd_glass17/icons/drcemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
           
    <ePixmap position="105,825" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />    
    <widget name="g17picon" position="124,841" size="150,90" zPosition="2" transparent="1" alphatest="on" />    	

		<widget position="322,859" size="97,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
			<convert type="g17EventTime">StartTime</convert>
		</widget>
		<widget position="442,861" size="466,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive3;30" valign="bottom" noWrap="1" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
			<convert type="EventName">Name</convert>
		</widget>
		<widget position="916,859" size="142,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="right" transparent="1">
			<convert type="g17EventTime">Remaining</convert>
		</widget>
		
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="321,829" size="762,21" zPosition="3" transparent="1" >
			<convert type="EventTime">Progress</convert>
		</widget>
    <widget name="slider_back" position="321,829" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />		
		<widget position="322,898" size="97,39" source="session.Event_Next" render="Label" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
			<convert type="g17EventTime">StartTime</convert>
		</widget>
		<widget position="442,900" size="466,39" source="session.Event_Next" render="g17EmptyEpg" font="Prive3;30" valign="bottom" noWrap="1" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
			<convert type="EventName">Name</convert>
		</widget>
		<widget position="916,898" size="142,39" source="session.Event_Next" render="Label" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" halign="right" transparent="1">
			<convert type="g17EventTime">Duration</convert>
		</widget>

    <widget name="subserv" position="1573,874" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1573,874" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
  	<widget name="dolby" position="1573,874" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
  	<widget name="txt" position="1573,874" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
		<widget name="tuner" position="1573,874" size="42,72" zPosition="1" alphatest="off"/>
    <widget name="HDD_state" position="1573,874" size="42,72" zPosition="1" alphatest="off" />    
		<widget position="1573,874" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on" >
			<convert type="g17ConditionalShowHide">Blink</convert>
		</widget> 
		
    <widget source="session.FrontendStatus" render="Progress" position="1626,828" size="7,112" zPosition="4" pixmap="hd_glass17/icons/bar.png" orientation="orBottomToTop" transparent="1" >
    <convert type="g17ExtraSource">SnrNum</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Progress" position="1801,828" size="7,112" zPosition="4" pixmap="hd_glass17/icons/bar.png" orientation="orBottomToTop" transparent="1" >
    <convert type="g17ExtraSource">AgcNum</convert>
    </widget>

    <ePixmap pixmap="hd_glass17/icons/bar_back_snr.png" position="1626,828" size="7,112" zPosition="1" alphatest="on"/>
    <ePixmap pixmap="hd_glass17/icons/bar_back.png" position="1801,828" size="7,112" zPosition="1" alphatest="on"/>

    <eLabel text="Snr:" font="Prive3;25" position="1648,846" zPosition="2" size="142,30" halign="left" backgroundColor="background" foregroundColor="#666666" transparent="1" />
    <eLabel text="Agc:" font="Prive3;25" position="1648,874" zPosition="2" size="142,30" halign="left" backgroundColor="background" foregroundColor="#666666" transparent="1" />
    <eLabel text="Ber:" font="Prive3;25" position="1648,903" zPosition="4" size="142,30" halign="left" backgroundColor="background" foregroundColor="#666666" transparent="1" />

    <widget source="session.FrontendStatus" render="Label" font="Prive3;25" position="1714,846" zPosition="5" backgroundColor="background" size="105,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;25" position="1714,874" zPosition="5" backgroundColor="background" size="105,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" 	font="Prive3;25" position="1714,903" zPosition="5" backgroundColor="background" size="105,30" halign="left" transparent="1"  >
    <convert type="g17ExtraSource">BerText</convert> 
    </widget>
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="caidPids" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" transparent="1" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" transparent="1" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />

	</screen>"""

g17_extraScreen["4"] = """

  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""
g17_extraScreen["4"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/4/infobar-ext3.png" alphatest="off"/>\n'
g17_extraScreen["4"]  += """<widget source="session.CurrentService" render="Label" position="322,762" size="120,52"  font="Prive3;42" halign="left" transparent="1" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2">	
    <convert type="g17ServiceNum">Number</convert>
    </widget>
    
    <widget position="442,762" size="757,52" source="session.CurrentService" render="Label" font="Prive3;42" valign="bottom" halign="left" noWrap="1" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
			<convert type="ServiceName">Name</convert>
		</widget>

		<ePixmap position="120,952" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png"/>
		<ePixmap position="960,952" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png"/>

    <widget name="TP_info" position="300,970" zPosition="1" size="783,34" font="Prive3;27" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>
    <widget name="TP_type" position="67,970" zPosition="1" size="279,34" font="Prive3;27" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>

		<widget name="Video_size"	font="Prive3;27" position="120,775" size="166,34" halign="center"  backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>

		<widget source="global.CurrentTime" 	render="Label" position="1611,762" size="135,52" font="Prive3;42" valign="top" halign="right" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
			<convert type="g17ClockToText">Default</convert>
		</widget>
		<widget source="global.CurrentTime" 	render="Label" position="1738,765" size="52,30" font="Prive3;30" valign="top" halign="right" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
			<convert type="g17ClockToText">Format::%S</convert>
		</widget>
		<widget source="global.CurrentTime" render="g17dateFormat" format="%A, %d %B %Y" position="945,775" size="660,30" font="Prive3;27" halign="right" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="1083,828" size="525,33" font="Prive3;27" transparent="1" halign="right" backgroundColor="background" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="Dcam" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="Decm" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm"	pixmap="hd_glass17/icons/irdemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D2_Demm"	pixmap="hd_glass17/icons/secemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D3_Demm"	pixmap="hd_glass17/icons/nagemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D4_Demm"	pixmap="hd_glass17/icons/viaemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D5_Demm"	pixmap="hd_glass17/icons/conemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D0_Demm"	pixmap="hd_glass17/icons/betemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D6_Demm"	pixmap="hd_glass17/icons/crwemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D7_Demm"	pixmap="hd_glass17/icons/drcemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
           
    <ePixmap position="105,825" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />    
    <widget name="g17picon" position="124,841" size="150,90" zPosition="2" transparent="1" alphatest="on" />    	

		<widget position="322,859" size="97,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
			<convert type="g17EventTime">StartTime</convert>
		</widget>
		<widget position="442,861" size="466,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive3;30" valign="bottom" noWrap="1" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
			<convert type="EventName">Name</convert>
		</widget>
		<widget position="916,859" size="142,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="right" transparent="1">
			<convert type="g17EventTime">Remaining</convert>
		</widget>
		
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="321,829" size="762,21" zPosition="3" transparent="1" >
			<convert type="EventTime">Progress</convert>
		</widget>
    <widget name="slider_back" position="321,829" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />		
		<widget position="322,898" size="97,39" source="session.Event_Next" render="Label" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
			<convert type="g17EventTime">StartTime</convert>
		</widget>
		<widget position="442,900" size="466,39" source="session.Event_Next" render="g17EmptyEpg" font="Prive3;30" valign="bottom" noWrap="1" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
			<convert type="EventName">Name</convert>
		</widget>
		<widget position="916,898" size="142,39" source="session.Event_Next" render="Label" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" halign="right" transparent="1">
			<convert type="g17EventTime">Duration</convert>
		</widget>

    <ePixmap position="1620,825" size="189,123" pixmap="hd_glass17/clk1.png" zPosition="1" alphatest="on" />    
		<widget source="global.CurrentTime" render="g17Ahours" position="1674,846" size="81,81" zPosition="4" alphatest="on" foregroundColor="#f23d21">
			<convert type="g17ExtraSource">secHand</convert>
		</widget>
		<widget source="global.CurrentTime" render="g17Ahours" position="1680,852" size="69,69" zPosition="3" foregroundColor="blue" alphatest="on">
			<convert type="g17ExtraSource">minHand</convert>
		</widget>
		<widget source="global.CurrentTime" render="g17Ahours" position="1692,864" size="45,45" zPosition="2" foregroundColor="blue" alphatest="on">
			<convert type="g17ExtraSource">hourHand</convert>
		</widget>

    <widget name="subserv" position="1576,874" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1576,874" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
  	<widget name="dolby" position="1576,874" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
  	<widget name="txt" position="1576,874" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
		<widget name="tuner" position="1576,874" size="42,72" zPosition="1" alphatest="off"/>
    <widget name="HDD_state" position="1576,874" size="42,72" zPosition="1" alphatest="off" />    
		<widget position="1576,874" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on" >
			<convert type="g17ConditionalShowHide">Blink</convert>
		</widget> 
		
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="caidPids" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" transparent="1" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" transparent="1" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />

	</screen>"""	

g17_extraScreen["5"] = """

  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""

g17_extraScreen["5"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/5/infobar-ext3.png" alphatest="off"/>\n'
g17_extraScreen["5"]  += """<widget source="session.CurrentService" render="Label" position="322,762" size="877,52" font="Prive3;42" halign="left" transparent="1" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2">	
    <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>    

		<ePixmap position="120,952" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png"/>
		<ePixmap position="960,952" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png"/>

    <widget name="TP_info" position="300,970" zPosition="1" size="783,34" font="Prive3;27" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>
    <widget name="TP_type" position="67,970" zPosition="1" size="279,34" font="Prive3;27" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>

		<widget name="Video_size"	font="Prive3;27" position="120,775" size="166,34" halign="center"  backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>

		<widget source="global.CurrentTime" 	render="Label" position="1611,762" size="135,52" font="Prive3;42" valign="top" halign="right" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
			<convert type="g17ClockToText">Default</convert>
		</widget>
		<widget source="global.CurrentTime" 	render="Label" position="1738,765" size="52,30" font="Prive3;30" valign="top" halign="right" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
			<convert type="g17ClockToText">Format::%S</convert>
		</widget>
		<widget source="global.CurrentTime" render="g17dateFormat" format="%A, %d %B %Y" position="945,775" size="660,30" font="Prive3;27" halign="right" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="1083,828" size="525,33" font="Prive3;27" transparent="1" halign="right" backgroundColor="background" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="Dcam" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="Decm" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm"	pixmap="hd_glass17/icons/irdemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D2_Demm"	pixmap="hd_glass17/icons/secemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D3_Demm"	pixmap="hd_glass17/icons/nagemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D4_Demm"	pixmap="hd_glass17/icons/viaemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D5_Demm"	pixmap="hd_glass17/icons/conemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D0_Demm"	pixmap="hd_glass17/icons/betemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D6_Demm"	pixmap="hd_glass17/icons/crwemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D7_Demm"	pixmap="hd_glass17/icons/drcemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
           
    <ePixmap position="105,825" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />    
    <widget name="g17picon" position="124,841" size="150,90" zPosition="2" transparent="1" alphatest="on" />     	

		<widget position="322,859" size="97,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
			<convert type="g17EventTime">StartTime</convert>
		</widget>
		<widget position="442,861" size="466,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive3;30" valign="bottom" noWrap="1" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
			<convert type="EventName">Name</convert>
		</widget>
		<widget position="916,859" size="142,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="right" transparent="1">
			<convert type="g17EventTime">Remaining</convert>
		</widget>
		
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="321,829" size="762,21" zPosition="3" transparent="1" >
			<convert type="EventTime">Progress</convert>
		</widget>
    <widget name="slider_back" position="321,829" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />		
		<widget position="322,898" size="97,39" source="session.Event_Next" render="Label" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
			<convert type="g17EventTime">StartTime</convert>
		</widget>
		<widget position="442,900" size="466,39" source="session.Event_Next" render="g17EmptyEpg" font="Prive3;30" valign="bottom" noWrap="1" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
			<convert type="EventName">Name</convert>
		</widget>
		<widget position="916,898" size="142,39" source="session.Event_Next" render="Label" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" halign="right" transparent="1">
			<convert type="g17EventTime">Duration</convert>
		</widget>

    <widget name="subserv" position="1573,874" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1573,874" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
  	<widget name="dolby" position="1573,874" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
  	<widget name="txt" position="1573,874" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
		<widget name="tuner" position="1573,874" size="42,72" zPosition="1" alphatest="off"/>
    <widget name="HDD_state" position="1573,874" size="42,72" zPosition="1" alphatest="off" />    
		<widget position="1573,874" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on" >
			<convert type="g17ConditionalShowHide">Blink</convert>
		</widget> 
		
    <widget source="session.FrontendStatus" render="Progress" position="1626,828" size="7,112" zPosition="4" pixmap="hd_glass17/icons/bar.png" orientation="orBottomToTop" transparent="1" >
    <convert type="g17ExtraSource">SnrNum</convert>
    </widget>

    <ePixmap pixmap="hd_glass17/icons/bar_back_snr.png" position="1626,828" size="7,112" zPosition="1" alphatest="on"/>

    <eLabel text="Snr:" font="Prive3;25" position="1648,846" zPosition="2" size="142,30" halign="left" backgroundColor="background" foregroundColor="#666666" transparent="1" />
    <eLabel text="Snr:" font="Prive3;25" position="1648,874" zPosition="2" size="142,30" halign="left" backgroundColor="background" foregroundColor="#666666" transparent="1" />
    <eLabel text="Ber:" font="Prive3;25" position="1648,903" zPosition="4" size="142,30" halign="left" backgroundColor="background" foregroundColor="#666666" transparent="1" />

    <widget source="session.FrontendStatus" render="Label" font="Prive3;25" position="1714,846" zPosition="5" backgroundColor="background" size="105,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrdB</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;25" position="1714,874" zPosition="5" backgroundColor="background" size="105,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" 	font="Prive3;25" position="1714,903" zPosition="5" backgroundColor="background" size="105,30" halign="left" transparent="1"  >
    <convert type="g17ExtraSource">BerText</convert> 
    </widget>
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />

	</screen>"""

g17_extraScreen["6"] = """

  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">

	  <widget source="session.CurrentService" render="Label" position="322,762" size="877,52" font="Prive3;42" halign="left" transparent="1" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2">	
    <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>

		<ePixmap position="120,952" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png"/>
		<ePixmap position="960,952" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png"/>

    <widget name="TP_info" position="300,970" zPosition="1" size="783,34" font="Prive3;27" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>
    <widget name="TP_type" position="67,970" zPosition="1" size="279,34" font="Prive3;27" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>

		<widget name="Video_size"	font="Prive3;27" position="120,775" size="166,34" halign="center"  backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>

		<widget source="global.CurrentTime" 	render="Label" position="1611,762" size="135,52" font="Prive3;42" valign="top" halign="right" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
			<convert type="g17ClockToText">Default</convert>
		</widget>
		<widget source="global.CurrentTime" 	render="Label" position="1738,765" size="52,30" font="Prive3;30" valign="top" halign="right" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
			<convert type="g17ClockToText">Format::%S</convert>
		</widget>
		<widget source="global.CurrentTime" render="g17dateFormat" format="%A, %d %B %Y" position="945,775" size="660,30" font="Prive3;27" halign="right" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="1083,828" size="525,33" font="Prive3;27" transparent="1" halign="right" backgroundColor="background" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="Dcam" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="Decm" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm"	pixmap="hd_glass17/icons/irdemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D2_Demm"	pixmap="hd_glass17/icons/secemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D3_Demm"	pixmap="hd_glass17/icons/nagemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D4_Demm"	pixmap="hd_glass17/icons/viaemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D5_Demm"	pixmap="hd_glass17/icons/conemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D0_Demm"	pixmap="hd_glass17/icons/betemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D6_Demm"	pixmap="hd_glass17/icons/crwemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D7_Demm"	pixmap="hd_glass17/icons/drcemm-fs8.png" position="1731,961" size="78,46" zPosition="3" alphatest="off"/>
           
    <ePixmap position="105,825" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />    
    <widget name="g17picon" position="124,841" size="150,90" zPosition="2" transparent="1" alphatest="on" />    	

		<widget position="322,859" size="97,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
			<convert type="g17EventTime">StartTime</convert>
		</widget>
		<widget position="442,861" size="466,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive3;30" valign="bottom" noWrap="1" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
			<convert type="EventName">Name</convert>
		</widget>
		<widget position="916,859" size="142,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="right" transparent="1">
			<convert type="g17EventTime">Remaining</convert>
		</widget>
		
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="321,829" size="762,21" zPosition="3" transparent="1" >
			<convert type="EventTime">Progress</convert>
		</widget>
    <widget name="slider_back" position="321,829" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />		
		<widget position="322,898" size="97,39" source="session.Event_Next" render="Label" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
			<convert type="g17EventTime">StartTime</convert>
		</widget>
		<widget position="442,900" size="466,39" source="session.Event_Next" render="g17EmptyEpg" font="Prive3;30" valign="bottom" noWrap="1" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
			<convert type="EventName">Name</convert>
		</widget>
		<widget position="916,898" size="142,39" source="session.Event_Next" render="Label" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" halign="right" transparent="1">
			<convert type="g17EventTime">Duration</convert>
		</widget>

    <widget name="subserv" position="1573,874" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1573,874" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
  	<widget name="dolby" position="1573,874" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
  	<widget name="txt" position="1573,874" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
		<widget name="tuner" position="1573,874" size="42,72" zPosition="1" alphatest="off"/>
    <widget name="HDD_state" position="1573,874" size="42,72" zPosition="1" alphatest="off" />    
		<widget position="1573,874" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on" >
			<convert type="g17ConditionalShowHide">Blink</convert>
		</widget>
		
    <widget source="session.FrontendStatus" render="Label" font="Prive3;21" position="1633,837" zPosition="2" backgroundColor="background" size="105,24" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;21" position="1705,837" zPosition="2" backgroundColor="background" size="105,24" halign="right" transparent="1" >
    <convert type="g17ExtraSource">SnrdB</convert>
    </widget>"""
g17_extraScreen["6"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/6/infobar-ext3.png" alphatest="off"/>\n'
g17_extraScreen["6"]  += '<ePixmap pixmap="'+PATH+'/6/snr-all.png" position="1626,829" size="192,114" zPosition="1" alphatest="off"/>\n'
g17_extraScreen["6"]  += '<ePixmap pixmap="'+PATH+'/6/snr-b.png" position="1699,921" size="46,21" zPosition="4" alphatest="off"/>\n'
g17_extraScreen["6"]  += """<widget source="session.FrontendStatus" render="g17Ahours" position="1645,862" size="150,150" zPosition="3" foregroundColor="yellow" alphatest="on">
		<convert type="g17ExtraSource">SnrAnalog</convert>
		</widget>
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />

	</screen>"""

g17_extraScreen["7"] = """

  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""
g17_extraScreen["7"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/7/infobar-ext4.png" alphatest="off"/>\n'

g17_extraScreen["7"]  += """<widget source="session.CurrentService" render="Label" position="322,729" size="120,52"  font="Prive3;42" halign="left" transparent="1" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2">	
    <convert type="g17ServiceNum">Number</convert>
    </widget>
    
    <widget position="442,729" size="757,52" source="session.CurrentService" render="Label" font="Prive3;42" valign="bottom" halign="left" noWrap="1" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
			<convert type="ServiceName">Name</convert>
		</widget>

		<ePixmap position="120,919" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png"/>
		<ePixmap position="960,919" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png"/>

    <widget name="TP_info" position="300,937" zPosition="1" size="783,34" font="Prive3;27" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>
    <widget name="TP_type" position="67,937" zPosition="1" size="279,34" font="Prive3;27" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>

		<widget name="Video_size"	font="Prive3;27" position="120,742" size="166,34" halign="center"  backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>

		<widget source="global.CurrentTime" 	render="Label" position="1611,729" size="135,52" font="Prive3;42" valign="top" halign="right" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
			<convert type="g17ClockToText">Default</convert>
		</widget>
		<widget source="global.CurrentTime" 	render="Label" position="1738,732" size="52,30" font="Prive3;30" valign="top" halign="right" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
			<convert type="g17ClockToText">Format::%S</convert>
		</widget>
		<widget source="global.CurrentTime" render="g17dateFormat" format="%A, %d %B %Y" position="945,742" size="660,30" font="Prive3;27" halign="right" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="1083,795" size="525,33" font="Prive3;27" transparent="1" halign="right" backgroundColor="background" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1731,928" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="Dcam" position="1731,928" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="Decm" position="1731,928" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm"	pixmap="hd_glass17/icons/irdemm-fs8.png" position="1731,928" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D2_Demm"	pixmap="hd_glass17/icons/secemm-fs8.png" position="1731,928" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D3_Demm"	pixmap="hd_glass17/icons/nagemm-fs8.png" position="1731,928" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D4_Demm"	pixmap="hd_glass17/icons/viaemm-fs8.png" position="1731,928" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D5_Demm"	pixmap="hd_glass17/icons/conemm-fs8.png" position="1731,928" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D0_Demm"	pixmap="hd_glass17/icons/betemm-fs8.png" position="1731,928" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D6_Demm"	pixmap="hd_glass17/icons/crwemm-fs8.png" position="1731,928" size="78,46" zPosition="3" alphatest="off"/>
    <widget name="D7_Demm"	pixmap="hd_glass17/icons/drcemm-fs8.png" position="1731,928" size="78,46" zPosition="3" alphatest="off"/>
           
    <ePixmap position="105,792" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />    
    <widget name="g17picon" position="124,808" size="150,90" zPosition="2" transparent="1" alphatest="on" />   	

		<widget position="322,826" size="97,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
			<convert type="g17EventTime">StartTime</convert>
		</widget>
		<widget position="442,828" size="466,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive3;30" valign="bottom" noWrap="1" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
			<convert type="EventName">Name</convert>
		</widget>
		<widget position="916,826" size="142,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="right" transparent="1">
			<convert type="g17EventTime">Remaining</convert>
		</widget>
		
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="321,796" size="762,21" zPosition="3" transparent="1" >
			<convert type="EventTime">Progress</convert>
		</widget>
    <widget name="slider_back" position="321,796" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />		
		<widget position="322,865" size="97,39" source="session.Event_Next" render="Label" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
			<convert type="g17EventTime">StartTime</convert>
		</widget>
		<widget position="442,867" size="466,39" source="session.Event_Next" render="g17EmptyEpg" font="Prive3;30" valign="bottom" noWrap="1" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
			<convert type="EventName">Name</convert>
		</widget>
		<widget position="916,865" size="142,39" source="session.Event_Next" render="Label" font="Prive3;33" valign="bottom" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" halign="right" transparent="1">
			<convert type="g17EventTime">Duration</convert>
		</widget>

    <widget name="subserv" position="1573,841" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1573,841" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
  	<widget name="dolby" position="1573,841" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
  	<widget name="txt" position="1573,841" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
		<widget name="tuner" position="1573,841" size="42,72" zPosition="1" alphatest="off"/>
    <widget name="HDD_state" position="1573,841" size="42,72" zPosition="1" alphatest="off" />    
		<widget position="1573,841" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on" >
			<convert type="g17ConditionalShowHide">Blink</convert>
		</widget> 
		
    <widget source="session.FrontendStatus" render="Progress" position="1626,795" size="7,112" zPosition="4" pixmap="hd_glass17/icons/bar.png" orientation="orBottomToTop" transparent="1" >
    <convert type="g17ExtraSource">SnrNum</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Progress" position="1801,795" size="7,112" zPosition="4" pixmap="hd_glass17/icons/bar.png" orientation="orBottomToTop" transparent="1" >
    <convert type="g17ExtraSource">AgcNum</convert>
    </widget>

    <ePixmap pixmap="hd_glass17/icons/bar_back_snr.png" position="1626,795" size="7,112" zPosition="1" alphatest="on"/>
    <ePixmap pixmap="hd_glass17/icons/bar_back.png" position="1801,795" size="7,112" zPosition="1" alphatest="on"/>

    <eLabel text="Snr:" font="Prive3;25" position="1648,813" zPosition="2" size="142,30" halign="left" backgroundColor="background" foregroundColor="#666666" transparent="1" />
    <eLabel text="Agc:" font="Prive3;25" position="1648,841" zPosition="2" size="142,30" halign="left" backgroundColor="background" foregroundColor="#666666" transparent="1" />
    <eLabel text="Ber:" font="Prive3;25" position="1648,870" zPosition="4" size="142,30" halign="left" backgroundColor="background" foregroundColor="#666666" transparent="1" />

    <widget source="session.FrontendStatus" render="Label" font="Prive3;25" position="1714,813" zPosition="5" backgroundColor="background" size="105,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;25" position="1714,841" zPosition="5" backgroundColor="background" size="105,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" 	font="Prive3;25" position="1714,870" zPosition="5" backgroundColor="background" size="105,30" halign="left" transparent="1"  >
    <convert type="g17ExtraSource">BerText</convert> 
    </widget>

		<ePixmap position="120,979" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png"/>
		<ePixmap position="960,979" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png"/>

    <widget position="511,988" size="1290,24" zPosition="3" name="ecmLineInfo" font="Prive3;24" halign="right" backgroundColor="background" transparent="1"/>
    <widget name="bitrate_info" position="120,988" zPosition="3" size="450,30" font="Prive3;24" halign="left" backgroundColor="background" transparent="1"/>
		<widget name="ecmlabels" font="Prive3;24" position="108,202" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,202" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,37"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,91"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,91"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,549"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,549"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />

	</screen>"""

g17_extraScreen["8"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="hd_glass17/general/infobar-ex.png" alphatest="off" />

  	<widget name="Video_size" font="Prive4;27" position="100,766" size="210,31" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />

    <widget source="session.CurrentService" render="Label" position="315,760" size="120,39" font="Prive4;33" halign="left" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2" valign="bottom">
      <convert type="g17ServiceNum">Number</convert>
    </widget>
    <widget position="435,754" size="757,48" source="session.CurrentService" render="Label" font="Prive4;39" valign="bottom" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="ServiceName">Name</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="937,766" size="660,30" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1609,754" size="135,48" font="Prive4;39" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1725,757" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <ePixmap position="111,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="130,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />   
  
    <widget name="Prov_temp_rpm" position="1075,826" size="525,33" font="Prive3;27" halign="right" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

    <ePixmap position="1620,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1639,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />    
    <widget name="weaTxt" position="1639,835" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
    
    <widget position="315,828" size="90,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,828" size="495,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,828" size="142,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" halign="right" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="313,867" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="313,867" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />    
    <widget position="315,892" size="90,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,892" size="495,39" source="session.Event_Next" render="g17EmptyEpg" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6" transparent="1" backgroundColor="background">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,892" size="142,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" halign="right" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1569,871" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1569,871" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1569,871" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
    <ePixmap position="120,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="960,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <widget name="TP_type" position="121,952" zPosition="2" size="293,30" font="Prive4;22" halign="left" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget name="TP_info" position="315,951" zPosition="1" size="735,30" font="Prive4;24" halign="center" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />

    <widget name="Dtype" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
          	
    <eLabel text="Snr: dB" font="Prive4;24" position="121,988" size="105,30" foregroundColor="un99bad6" transparent="1" backgroundColor="background"/>
    <widget source="session.FrontendStatus" render="Label" position="226,988" size="90,30" font="Prive4;24" zPosition="5" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17ExtraSource">SnrdB</convert>
    </widget>
    <eLabel text="Snr:" position="319,988" size="60,30" font="Prive4;24" foregroundColor="un99bad6" transparent="1" backgroundColor="background"/>
    <widget source="session.FrontendStatus" render="Label" position="379,988" size="90,30" font="Prive4;24" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="469,988" size="60,30" font="Prive4;24" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="529,988" size="90,30" font="Prive4;24" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <eLabel text="Ber:" position="619,988" size="60,30" font="Prive4;24" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="679,988" size="90,30" font="Prive4;24" foregroundColor="unefb2b2" transparent="1" backgroundColor="background">
      <convert type="g17ExtraSource">BerText</convert>
    </widget>
    <widget name="ecmLineInfo" position="780,994" size="1017,24" font="Prive4;18" noWrap="1" halign="right" backgroundColor="background" foregroundColor="unb2e0b4" zPosition="5" transparent="1" />
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>	
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />

	</screen>"""
	
g17_extraScreen["9"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="hd_glass17/general/infobar-ex.png" alphatest="off" />

  	<widget name="Video_size" font="Prive4;27" position="100,766" size="210,33" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />

    <widget source="session.CurrentService" render="Label" position="315,760" size="120,39" font="Prive4;33" halign="left" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2" valign="bottom">
      <convert type="g17ServiceNum">Number</convert>
    </widget>
    <widget position="457,754" size="757,48" source="session.CurrentService" render="Label" font="Prive4;39" valign="bottom" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="ServiceName">Name</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="907,766" size="693,30" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1609,754" size="135,48" font="Prive4;39" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1725,757" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <ePixmap position="111,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="130,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />  
  
    <widget name="Prov_temp_rpm" position="1075,826" size="525,33" font="Prive4;27" halign="right" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />

    <ePixmap position="1620,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1639,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />    
    <widget name="weaTxt" position="1639,835" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
    
    <widget position="315,828" size="90,39" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,828" size="495,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,828" size="142,39" source="session.Event_Now" render="Label" zPosition="1" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="313,867" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="313,867" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />    
    <widget position="315,892" size="90,39" source="session.Event_Next" render="Label" font="Prive4;27" transparent="1" backgroundColor="background" valign="bottom" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,892" size="495,39" source="session.Event_Next" render="g17EmptyEpg" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,892" size="142,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1569,871" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1569,871" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1569,871" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
    <ePixmap position="120,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="960,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <widget name="TP_type" position="121,952" zPosition="2" size="293,30" font="Prive4;24" transparent="1" backgroundColor="background" halign="left" foregroundColor="un99bad6" />
    <widget name="TP_info" position="315,951" zPosition="1" size="735,30" font="Prive4;24" transparent="1" backgroundColor="background" halign="center" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
          	
    <eLabel text="Snr:" font="Prive4;24" position="121,988" size="105,30" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="181,988" size="90,30" font="Prive4;24" zPosition="5" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="271,988" size="60,30" font="Prive4;24" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="331,988" size="90,30" font="Prive4;24" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <widget name="bitrate_info" position="421,988" zPosition="8" size="750,30" font="Prive3;24" halign="left" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1"/>

    <widget name="ecmLineInfo" position="780,994" size="1017,24" font="Prive4;18" noWrap="1" halign="right" backgroundColor="background" transparent="1" foregroundColor="unb2e0b4" zPosition="5" />
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>	
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />

	</screen>"""
	
g17_extraScreen["10"] = """

  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="hd_glass17/general/infobar-ex.png" alphatest="off" />

    <widget source="session.CurrentService" render="Label" position="285,760" size="120,39" font="Prive4;33" halign="right" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2" valign="bottom">
      <convert type="g17ServiceNum">Number</convert>
    </widget>
    <widget position="435,754" size="757,48" source="session.CurrentService" render="Label" font="Prive4;39" valign="bottom" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="ServiceName">Name</convert>
    </widget>
    <ePixmap position="120,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="960,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <widget name="TP_info" position="318,951" zPosition="1" size="750,30" font="Prive4;24" halign="left" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />
    <widget name="TP_type" position="121,952" zPosition="2" size="293,30" font="Prive4;22" halign="left" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />
    <widget name="Video_size" font="Prive4;27" position="115,766" size="180,33" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1609,754" size="135,48" font="Prive4;39" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1725,757" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="937,766" size="660,30" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="1075,826" size="525,33" font="Prive4;27" halign="right" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    
    <ePixmap position="111,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="130,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />

    <widget position="315,858" size="90,39" source="session.Event_Now" render="Label" zPosition="1" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,858" size="495,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,858" size="142,39" source="session.Event_Now" render="Label" zPosition="1" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="313,837" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="313,837" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />
    <widget position="315,892" size="90,39" source="session.Event_Next" render="Label" font="Prive4;27" transparent="1" backgroundColor="background" valign="bottom" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,892" size="495,39" source="session.Event_Next" render="g17EmptyEpg" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,892" size="142,39" source="session.Event_Next" render="Label" font="Prive4;27" transparent="1" backgroundColor="background" valign="bottom" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    <ePixmap position="1620,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1639,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />
     <widget name="weaTxt" position="1639,835" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />

    <widget name="subserv" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1569,871" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1569,871" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1569,871" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
    <eLabel text="Snr:" font="Prive4;24" position="121,988" size="105,30" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="181,988" size="90,30" font="Prive4;24" transparent="1" backgroundColor="background" zPosition="5" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="271,988" size="60,30" font="Prive4;24" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="331,988" size="90,30" font="Prive4;24" transparent="1" backgroundColor="background" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <widget name="bitrate_info" position="421,988" zPosition="8" size="750,30" font="Prive3;24" halign="left" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1"/>
    <widget name="ecmLineInfo" position="780,994" size="1017,24" font="Prive4;18" noWrap="1" halign="right" backgroundColor="background" foregroundColor="unb2e0b4" zPosition="5" transparent="1" />

		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />

  </screen>"""	
	
g17_extraScreen["11"] = """

  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="hd_glass17/general/infobar-ex.png" alphatest="off" />

    <widget source="session.CurrentService" render="Label" position="285,760" size="120,39" font="Prive4;33" halign="right" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2" valign="bottom">
      <convert type="g17ServiceNum">Number</convert>
    </widget>
    <widget position="435,754" size="757,48" source="session.CurrentService" render="Label" font="Prive4;39" valign="bottom" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="ServiceName">Name</convert>
    </widget>
    <ePixmap position="120,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="960,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <widget name="TP_info" position="318,951" zPosition="1" size="750,30" font="Prive4;27" halign="left" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />
    <widget name="TP_type" position="111,953" zPosition="2" size="293,30" font="Prive4;23" halign="left" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />

    <widget name="Video_size" font="Prive4;27" position="115,766" size="180,33" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1609,754" size="135,48" font="Prive4;39" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1725,757" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="937,766" size="660,30" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="1075,826" size="525,33" font="Prive4;27" halign="right" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />

    <ePixmap position="111,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="130,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />

    <widget position="315,858" size="90,39" source="session.Event_Now" render="Label" zPosition="1" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,858" size="495,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,858" size="142,39" source="session.Event_Now" render="Label" zPosition="1" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="313,837" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="313,837" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />
    <widget position="315,892" size="90,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,892" size="495,39" source="session.Event_Next" render="g17EmptyEpg" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,892" size="142,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    <ePixmap position="1620,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1639,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />
    <widget name="weaTxt" position="1639,835" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />

    <widget name="subserv" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1569,871" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1569,871" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1569,871" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    <widget name="Dtype" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    
    <widget name="ecmLineInfo" position="780,994" size="1017,24" font="Prive4;18" noWrap="1" transparent="1" halign="right" backgroundColor="background" foregroundColor="unb2e0b4" zPosition="5" />
    <eLabel text="Snr: dB" font="Prive4;27" position="111,988" size="125,30" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="226,988" size="90,30" font="Prive4;27" zPosition="5" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
    <convert type="g17ExtraSource">SnrdB</convert>
    </widget>
    <eLabel text="Snr:" position="319,988" size="60,30" font="Prive4;27" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="379,988" size="90,30" font="Prive4;27" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="474,988" size="60,30" font="Prive4;27" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="543,988" size="90,30" font="Prive4;27" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
    <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <eLabel text="Ber:" position="633,988" size="60,30" font="Prive4;27" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="693,988" size="90,30" font="Prive4;27" foregroundColor="unefb2b2" transparent="1" backgroundColor="background">
    <convert type="g17ExtraSource">BerText</convert>
    </widget>
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="bitrate_info" position="780,951" size="1017,30" zPosition="5" font="Prive4;25" halign="right" backgroundColor="background" foregroundColor="un99bad6" transparent="1"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />

  </screen>"""
  
g17_extraScreen["12"] = """

  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <ePixmap position="0,0" zPosition="-2" size="1927,1080" pixmap="hd_glass17/general/infobar.png" alphatest="off" />

    <widget source="session.CurrentService" render="Label" position="106,822" size="210,52" font="Prive3;39" halign="center" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2">
      <convert type="g17ServiceNum">Number</convert>
    </widget>
    <widget position="315,822" size="757,52" source="session.CurrentService" render="Label" font="Prive3;39" valign="bottom" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="ServiceName">Name</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1609,822" size="135,48" font="Prive3;39" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1725,825" size="69,33" font="Prive3;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="937,832" size="660,33" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <ePixmap position="111,894" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="130,910" size="150,90" zPosition="2" transparent="1" alphatest="on" />

    <widget position="315,933" size="90,39" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" zPosition="1" font="Prive3;27" valign="bottom" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,933" size="495,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" emptyText="No EPG data available" zPosition="-1" font="Prive3;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,933" size="142,39" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" zPosition="1" font="Prive3;27" valign="bottom" foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget name="slider_back" position="313,912" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="313,912" size="762,21" zPosition="1" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget position="315,967" size="90,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive3;27" valign="bottom" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,967" size="495,39" source="session.Event_Next" render="g17EmptyEpg" transparent="1" backgroundColor="background" emptyText="No EPG data available" font="Prive3;27" valign="bottom" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,967" size="142,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive3;27" valign="bottom" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    <ePixmap position="1620,894" size="189,123" pixmap="hd_glass17/clk1.png" zPosition="1" alphatest="on" />
    <widget source="global.CurrentTime" render="g17Ahours" position="1674,915" size="81,81" zPosition="4" alphatest="on" foregroundColor="red">
      <convert type="g17ExtraSource">secHand</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17Ahours" position="1680,921" size="69,69" zPosition="3" foregroundColor="blue" alphatest="on">
      <convert type="g17ExtraSource">minHand</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17Ahours" position="1692,933" size="45,45" zPosition="2" foregroundColor="blue" alphatest="on">
      <convert type="g17ExtraSource">hourHand</convert>
    </widget>

    <widget name="HDD_state" position="1297,915" size="42,72" zPosition="2" alphatest="off" />    
    <widget name="Dtype" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1723,951" size="0,0" zPosition="3" alphatest="off" />

    <widget position="1297,915" size="39,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" alphatest="on" zPosition="1">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    <widget source="session.FrontendInfo" render="g17TunersLabel" font="Regular2;31" position="1350,907" alphatest="off" size="247,78" tuners="5" ActiveTunerColor="#0000d100" backgroundColor="background" BackgroundActiveTunerColor="#00ecb100" zPosition="2"/>

    <widget source="session.FrontendStatus" render="Progress" position="1095,898" size="7,112" zPosition="4" pixmap="hd_glass17/icons/bar.png" orientation="orBottomToTop" transparent="1">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <ePixmap pixmap="hd_glass17/icons/bar_back_snr.png" position="1095,898" size="7,112" zPosition="1" backgroundColor="background" alphatest="on" />
    <widget source="session.FrontendStatus" render="Progress" position="1267,898" size="7,112" zPosition="4" pixmap="hd_glass17/icons/bar.png" orientation="orBottomToTop" transparent="1">
      <convert type="g17ExtraSource">AgcNum</convert>
    </widget>
    <ePixmap pixmap="hd_glass17/icons/bar_back.png" position="1267,898" size="7,112" zPosition="1" backgroundColor="background" alphatest="on" />
    <eLabel text="Snr:" font="Prive3;21" position="1125,895" zPosition="2" size="60,30" halign="left" foregroundColor="un99bad6" backgroundColor="background" transparent="1"/>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;21" position="1188,895" backgroundColor="background" transparent="1" zPosition="5" size="75,30" halign="left" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">SnrdB</convert>
    </widget>
    <eLabel text="Snr:" position="1125,925" size="60,30" font="Prive3;21" halign="left" backgroundColor="background" transparent="1" foregroundColor="un99bad6" />
    <widget source="session.FrontendStatus" render="Label" position="1188,925" size="75,30" backgroundColor="background" transparent="1" font="Prive3;21" halign="left" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="1125,955" size="60,30" font="Prive3;21" halign="left" backgroundColor="background" transparent="1" foregroundColor="un99bad6" />
    <widget source="session.FrontendStatus" render="Label" position="1188,955" size="75,30" backgroundColor="background" transparent="1" font="Prive3;21" halign="left" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <eLabel text="Ber:" position="1125,985" size="60,30" font="Prive3;21" halign="left" backgroundColor="background" transparent="1" foregroundColor="un99bad6" />
    <widget source="session.FrontendStatus" render="Label" position="1188,985" size="75,30" backgroundColor="background" transparent="1" font="Prive3;21" halign="left" foregroundColor="unefb2b2">
      <convert type="g17ExtraSource">BerText</convert>
    </widget>
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />

  </screen>""" 

g17_extraScreen["13"] = """
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""
g17_extraScreen["13"]  += '<ePixmap position="0,649" size="1920,436" zPosition="-2" pixmap="'+PATH+'/13/infobar2.png" alphatest="off" />\n'
g17_extraScreen["13"]  += '<ePixmap position="484,844" zPosition="0" size="1385,198" pixmap="'+PATH+'/13/Frame172.png" alphatest="blend" />\n'
g17_extraScreen["13"]  += """  
    <eLabel backgroundColor="background" position="496,855" size="1161,177" zPosition="-1" />
    <widget position="503,777" size="825,87" source="session.CurrentService" render="Label" font="Prive3;48" zPosition="0" valign="top" halign="left" noWrap="1" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" >
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <eLabel position="503,931" zPosition="8" size="1346,1" backgroundColor="#1546AF" transparent="0" />
    <widget name="TP_type" position="678,979" zPosition="2" size="271,24" font="Prive4;21" halign="left"  backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget name="TP_info" position="890,979" zPosition="1" size="465,24" font="Prive4;21" halign="left" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget name="Video_size" font="Prive4;21" position="503,979" size="150,24" halign="left" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget source="global.CurrentTime" render="Label" position="1671,754" size="135,52" font="Prive3;39" valign="top" halign="right" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" >
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1798,756" size="52,30" font="Prive3;27" valign="top" halign="right" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" >
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%d.%B %Y" position="1579,796" size="270,30" font="Prive3;27" halign="right" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Dtype" position="1777,937" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1777,937" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1777,937" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1777,937" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1777,937" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1777,937" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1777,937" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1777,937" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1777,937" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1777,937" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1777,937" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1777,937" size="78,46" zPosition="3" alphatest="off" />
    
    <ePixmap position="50,780" size="426,262" pixmap="hd_glass17/frame/Frame13.png" zPosition="1" transparent="1" alphatest="on" />
    <widget name="g17picon" position="63,791" size="400,240" zPosition="2" transparent="1" alphatest="blend" />

    <widget position="503,859" size="90,30" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;24" valign="bottom" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" >
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="592,859" size="597,30" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" font="Prive4;24" valign="bottom" noWrap="1" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" >
      <convert type="EventName">Name</convert>
    </widget>
		<widget position="1191,859" size="142,30" source="session.Event_Now" render="Label" font="Prive4;24" valign="bottom" halign="right" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" >
			<convert type="g17EventTime">Remaining</convert>
		</widget>

    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_390.png" position="603,888" size="630,12" zPosition="6" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <eLabel position="603,894" zPosition="8" size="630,1" backgroundColor="#1546AF" transparent="0" />
    <widget position="503,901" size="90,30" source="session.Event_Next" render="Label" font="Prive4;24" valign="bottom" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" >
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="592,901" size="597,30" source="session.Event_Next" render="g17EmptyEpg" font="Prive4;24" valign="bottom" noWrap="1" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" >
      <convert type="EventName">Name</convert>
    </widget>
		<widget position="1191,901" size="142,30" source="session.Event_Next" render="Label" font="Prive4;24" valign="bottom" halign="right" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" >
			<convert type="g17EventTime">Duration</convert>
		</widget>

    <widget name="subserv" position="1816,862" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1816,862" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1816,862" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1816,862" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1816,862" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1816,862" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1569,871" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1816,862" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1816,862" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
    <widget name="Prov_temp_rpm" position="503,942" size="525,30" font="Prive4;24" halign="left" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />    

    <widget name="ecmLineInfo" position="503,1006" size="1346,24" font="Prive4;19" noWrap="1" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
   
  <eLabel text="Snr:" font="Prive4;21" position="1578,979" size="52,30" halign="left"  backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="1627,979" size="75,30" font="Prive4;21" halign="left" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="1720,979" size="52,30" font="Prive4;21" halign="left"  backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="1770,979" size="82,30" font="Prive4;21" halign="left" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>

		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="caidPids" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" transparent="1" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    
  </screen>""" 

g17_extraScreen["14"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="hd_glass17/general/infobar-ex.png" alphatest="off" />

  	<widget name="Video_size" font="Prive4;28" position="100,766" size="217,33" halign="center" backgroundColor="lightblue" transparent="1" />

    <widget position="315,757" size="757,48" source="session.CurrentService" render="Label" font="Prive4;37" valign="bottom" halign="left" noWrap="1" backgroundColor="black" foregroundColor="red" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>

    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="937,762" size="660,30" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1609,757" size="135,48" font="Prive4;36" valign="top" halign="right"  backgroundColor="black" foregroundColor="white" shadowColor="#551A8B" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1725,760" size="69,39" font="Prive4;30" valign="top" halign="right"  backgroundColor="black" foregroundColor="white" shadowColor="#551A8B" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <ePixmap position="111,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="130,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />   
  
    <widget name="Prov_temp_rpm" position="1218,826" size="607,37" font="Prive4;27" halign="center" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />
           
    <widget position="315,828" size="112,39" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" zPosition="1" font="Prive4;31" valign="bottom" foregroundColor="green">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="426,828" size="498,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="-1" font="Prive4;31" valign="bottom" noWrap="1" foregroundColor="yellow">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,828" size="150,39" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" zPosition="1" font="Prive4;31" valign="bottom" foregroundColor="green" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="313,874" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="313,874" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />    
    <widget position="315,897" size="112,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;31" valign="bottom" foregroundColor="yellow">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="426,897" size="505,39" source="session.Event_Next" render="g17EmptyEpg" transparent="1" backgroundColor="background" font="Prive4;31" valign="bottom" noWrap="1" foregroundColor="green">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,897" size="150,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;31" valign="bottom" foregroundColor="yellow" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1780,871" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1780,871" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1780,871" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1780,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1780,871" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1780,871" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1780,871" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1065,771" size="21,21" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/record.png" zPosition="2" alphatest="off">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
        
    <ePixmap position="120,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="960,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <widget name="TP_type" position="121,952" zPosition="2" size="293,30" font="Prive4;22" transparent="1" backgroundColor="background" halign="left" foregroundColor="un99bad6" />
    <widget name="TP_info" position="315,951" zPosition="1" size="735,30" font="Prive4;24" transparent="1" backgroundColor="background" halign="center" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1747,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1747,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1747,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1747,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1747,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1747,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1747,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1747,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1747,944" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1747,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1747,951" size="78,46" zPosition="3" alphatest="off" />
      	
    <widget source="session.FrontendStatus" render="Progress" position="1080,822" size="7,112" zPosition="4" pixmap="hd_glass17/icons/bar.png" orientation="orBottomToTop" transparent="1" >
    <convert type="g17ExtraSource">SnrNum</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Progress" position="1218,822" size="7,112" zPosition="4" pixmap="hd_glass17/icons/bar.png" orientation="orBottomToTop" transparent="1" >
    <convert type="g17ExtraSource">AgcNum</convert>
    </widget>

    <ePixmap pixmap="hd_glass17/icons/bar_back_snr.png" position="1080,822" size="7,112" zPosition="1" alphatest="on"/>
    <ePixmap pixmap="hd_glass17/icons/bar_back.png" position="1218,822" size="7,112" zPosition="1" alphatest="on"/>

    <eLabel text="Snr:" font="Prive3;22" position="1095,834" zPosition="2" size="142,30" halign="left" backgroundColor="background" foregroundColor="green" transparent="1" />
    <eLabel text="Agc:" font="Prive3;22" position="1095,864" zPosition="2" size="142,30" halign="left" backgroundColor="background" foregroundColor="yellow" transparent="1" />
    <eLabel text="Ber:" font="Prive3;22" position="1095,894" zPosition="4" size="142,30" halign="left" backgroundColor="background" foregroundColor="red" transparent="1" />

    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="1147,834" zPosition="5" backgroundColor="background" foregroundColor="white" size="105,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="1147,864" zPosition="5" backgroundColor="background" foregroundColor="white" size="105,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="1147,894" zPosition="5" backgroundColor="background" foregroundColor="white" size="105,30" halign="left" transparent="1"  >
    <convert type="g17ExtraSource">BerText</convert> 
    </widget>
  
    <widget name="bitrate_info" position="120,988" zPosition="8" size="750,30" font="Prive3;24" halign="left" backgroundColor="background" foregroundColor="red" transparent="1"/>

    <widget name="ecmLineInfo" position="585,991" size="1230,25" font="Prive4;22" noWrap="1" halign="right" foregroundColor="red" zPosition="5" transparent="1" backgroundColor="background" />
		<widget name="ecmlabels" font="Prive3;24" position="100,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="183,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="52,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="112,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="310,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="112,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="311,572"  size="150,90"  zPosition="2" alphatest="on"/>   
	 <widget  name="caidPids" transparent="1" position="529,157" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="499,97"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="-1" />  	 	
    <widget name="active_caidPid" transparent="1" position="529,157" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="499,163"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />

	</screen>"""   
	
g17_extraScreen["15"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="hd_glass17/general/infobar-ex.png" alphatest="off" />

  	<widget name="Video_size" font="Prive4;28" position="100,766" size="217,33" halign="center" backgroundColor="lightblue" transparent="1" />

    <widget position="315,757" size="757,48" source="session.CurrentService" render="Label" font="Prive4;37" valign="bottom" halign="left" noWrap="1" backgroundColor="black" foregroundColor="red" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="937,762" size="660,30" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1609,757" size="135,48" font="Prive4;36" valign="top" halign="right" backgroundColor="black" foregroundColor="red" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1725,760" size="69,34" font="Prive4;30" valign="top" halign="right" backgroundColor="black" foregroundColor="blue" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <ePixmap position="111,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="130,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />   
  
    <widget name="Prov_temp_rpm" position="1027,832" size="607,37" font="Prive4;27" halign="right" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />

    <ePixmap position="1635,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1654,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />    
    <widget name="weaTxt" position="1654,835" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
    
    <widget position="315,828" size="112,39" source="session.Event_Now" render="Label" zPosition="1" transparent="1" backgroundColor="background" font="Prive4;31" valign="bottom" foregroundColor="green">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="426,828" size="495,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="-1" font="Prive4;31" valign="bottom" noWrap="1" foregroundColor="yellow">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,828" size="150,39" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" zPosition="1" font="Prive4;31" valign="bottom" foregroundColor="green" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="313,874" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="313,874" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />    
    <widget position="315,892" size="112,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;31" valign="bottom" foregroundColor="yellow">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="426,892" size="495,39" source="session.Event_Next" render="g17EmptyEpg" transparent="1" backgroundColor="background" font="Prive4;31" valign="bottom" noWrap="1" foregroundColor="green">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,892" size="150,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;31" valign="bottom" foregroundColor="yellow" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1597,871" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1597,871" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1597,871" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1597,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1597,871" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1597,871" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1597,871" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1597,871" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
        
    <ePixmap position="120,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="960,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <widget name="TP_type" position="121,952" zPosition="2" size="293,30" font="Prive4;22" halign="left" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />
    <widget name="TP_info" position="315,951" zPosition="1" size="735,30" font="Prive4;24" halign="center" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1734,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1734,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1734,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1734,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1734,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1734,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1734,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1734,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1734,944" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1734,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1734,951" size="78,46" zPosition="3" alphatest="off" />
      	
  	<widget source="session.FrontendStatus" render="Progress" position="195,1005" size="300,7" zPosition="2" pixmap="hd_glass17/slider/sigbar.png" transparent="1" >
    <convert type="g17ExtraSource">SnrNum</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Progress" position="675,1005" size="300,7" zPosition="2" pixmap="hd_glass17/slider/sigbar.png" transparent="1" >
    <convert type="g17ExtraSource">AgcNum</convert>
    </widget>

    <ePixmap pixmap="hd_glass17/slider/sigsnrbar_back.png" position="195,1005" size="300,7" zPosition="1" alphatest="on"/>
    <ePixmap pixmap="hd_glass17/slider/sigbar_back.png" position="675,1005" size="300,7" zPosition="1" alphatest="on"/>

    <eLabel text="Ber:" font="Prive3;27" position="1095,990" zPosition="4" size="142,30" halign="left" backgroundColor="background" foregroundColor="red" transparent="1" />

    <widget source="session.FrontendStatus" render="Label" 	font="Prive3;27" position="1155,990" zPosition="5" backgroundColor="background" foregroundColor="white" size="105,30" halign="left" transparent="1"  >
    <convert type="g17ExtraSource">BerText</convert> 
    </widget>
  
    <eLabel text="Snr:" font="Prive4;27" position="126,988" size="60,30" foregroundColor="green" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="510,988" size="75,33" transparent="1" font="Prive4;27" zPosition="1" backgroundColor="background" foregroundColor="white">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="607,988" size="60,30" font="Prive4;27" foregroundColor="yellow" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="990,988" size="75,30" transparent="1" font="Prive4;27" backgroundColor="background" foregroundColor="white">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    
    <widget name="bitrate_info" position="1377,991" zPosition="8" size="750,30" font="Prive3;27" halign="left" backgroundColor="background" foregroundColor="red" transparent="1"/>
		<widget name="ecmlabels" font="Prive3;24" position="100,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="183,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="52,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="112,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="310,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="112,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="310,572"  size="150,90"  zPosition="2" alphatest="on"/> 
    <widget  name="caidPids" transparent="1" position="529,157" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="499,97"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="-1" />  	 	
    <widget name="active_caidPid" transparent="1" position="529,157" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="499,163"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />

	</screen>"""
  
g17_extraScreen["16"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">

    <ePixmap position="73,759" size="189,123" pixmap="hd_glass17/frame_hd4.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="93,775" size="150,90" zPosition="2" transparent="1" alphatest="on" />

    <ePixmap position="1656,759" size="189,123" pixmap="hd_glass17/frame_hd4.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1675,775" size="150,90" zPosition="2" transparent="1" alphatest="on" />    
    <widget name="weaTxt" position="1675,775" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
    
  	<widget name="Video_size" font="Prive4;25" position="73,720" size="189,37" valign="top" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget position="457,711" size="780,42" source="session.CurrentService" render="Label" font="Prive4;36" valign="top" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="ServiceName">Name</convert>
    </widget>
    
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="1081,720" size="660,30" font="Prive3;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1701,720" size="135,37" font="Prive4;25" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>      
    
    <widget position="270,766" size="150,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;31" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="378,766" size="885,45" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive4;34" halign="left" valign="top" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1242,766" size="157,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;31" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget name="slider_back" position="270,817" size="1129,15" pixmap="hd_glass17/slider/slider_back4.png" zPosition="2" transparent="1" alphatest="on" />    
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main4.png" position="270,817" size="1129,15" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    
    <widget position="270,840" size="150,39" source="session.Event_Next" render="Label" font="Prive4;31" valign="top" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="378,840" size="885,45" source="session.Event_Next" render="g17EmptyEpg" font="Prive4;34" halign="left" valign="top" noWrap="1" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1242,840" size="157,39" source="session.Event_Next" render="Label" font="Prive4;31" valign="top" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" halign="right" transparent="1">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="TP_info" position="97,889" zPosition="1" size="637,34" font="Prive4;22" valign="top" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget position="1423,888" size="397,34" source="session.CurrentService" render="Label" font="Prive4;24" valign="top" halign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="ServiceName">Provider</convert>
    </widget>
    <widget name="ecmLineInfo" position="769,994" size="1066,27" font="Prive4;19" backgroundColor="background" noWrap="1" valign="top" halign="right" transparent="1" />

    <widget name="subserv" position="712,949" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="712,949" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="712,949" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="712,949" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="712,949" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="712,949" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="712,949" size="42,72" zPosition="1" alphatest="off" />    
		<widget position="712,949" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on" >
			<convert type="g17ConditionalShowHide">Blink</convert>
		</widget>
		
    <widget name="Dtype" position="1768,949" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1768,949" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1768,949" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1768,949" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1768,949" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1768,949" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1768,949" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1768,949" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1768,949" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1768,949" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1768,949" size="78,46" zPosition="3" alphatest="off" />
     	
    <widget source="session.FrontendStatus" render="Label" font="Prive3;21" position="1449,766" zPosition="2" backgroundColor="background" size="105,24" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;21" position="1521,766" zPosition="2" backgroundColor="background" size="105,24" halign="right" transparent="1" >
    <convert type="g17ExtraSource">SnrdB</convert>
    </widget>

		<widget source="session.FrontendStatus" render="g17Ahours" position="1461,792" size="150,150" zPosition="3" foregroundColor="yellow" alphatest="on">
		<convert type="g17ExtraSource">SnrAnalog</convert>
		</widget>

		<widget name="ecmlabels" font="Prive3;24" position="97,195" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="180,195" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="picProv" position="109,84"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="307,84"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="109,543"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="307,543"  size="150,90"  zPosition="2" alphatest="on"/>	
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />"""
g17_extraScreen["16"]  += '<ePixmap position="0,702" zPosition="-2" size="1920,333" pixmap="'+PATH+'/16/infobar4.png" alphatest="off" />\n'
g17_extraScreen["16"]  += '<ePixmap pixmap="'+PATH+'/16/snr-all.png" position="1441,759" size="192,114" zPosition="1" alphatest="off"/>\n'
g17_extraScreen["16"]  += '<ePixmap pixmap="'+PATH+'/16/snr-b.png" position="1515,850" size="46,21" zPosition="4" alphatest="off"/>\n'
g17_extraScreen["16"]  += '<widget name="back_enhanced" position="49,30"  size="465,660" pixmap="'+PATH+'/16/back_enhanced4-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["16"]  += '<widget name="caidPids_back" alphatest="off" position="1609,45"  size="255,600" pixmap="'+PATH+'/16/back_caidPids4-fs8.png" zPosition="0" />\n'
g17_extraScreen["16"]  += '<widget name="caidPids_end" alphatest="off" position="1609,115"  size="255,27" pixmap="'+PATH+'/16/end_caidPids4-fs8.png" zPosition="3" />\n'
g17_extraScreen["16"]  += """</screen>"""
	
g17_extraScreen["17"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">

    <ePixmap position="73,849" size="189,123" pixmap="hd_glass17/frame_hd4.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="93,865" size="150,90" zPosition="2" transparent="1" alphatest="on" />

    <ePixmap position="1656,849" size="189,123" pixmap="hd_glass17/frame_hd4.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1675,865" size="150,90" zPosition="2" transparent="1" alphatest="on" />    
    <widget name="weaTxt" position="1675,865" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
    
  	<widget name="Video_size" font="Prive4;25" position="73,810" size="189,37" valign="top" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget position="457,801" size="780,42" source="session.CurrentService" render="Label" font="Prive4;36" valign="top" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="ServiceName">Name</convert>
    </widget>
    
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="1081,810" size="660,30" font="Prive3;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1701,810" size="135,37" font="Prive4;25" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>      
    
    <widget position="270,856" size="150,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;31" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="378,856" size="885,45" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive4;34" halign="left" valign="top" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1242,856" size="157,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;31" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget name="slider_back" position="270,907" size="1129,15" pixmap="hd_glass17/slider/slider_back4.png" zPosition="2" transparent="1" alphatest="on" />    
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main4.png" position="270,907" size="1129,15" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    
    <widget position="270,930" size="150,39" source="session.Event_Next" render="Label" font="Prive4;31" valign="top" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="378,930" size="885,45" source="session.Event_Next" render="g17EmptyEpg" font="Prive4;34" halign="left" valign="top" noWrap="1" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1242,930" size="157,39" source="session.Event_Next" render="Label" font="Prive4;31" valign="top" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" halign="right" transparent="1">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="TP_info" position="97,979" zPosition="1" size="637,34" font="Prive4;22" valign="top" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget position="1423,978" size="397,34" source="session.CurrentService" render="Label" font="Prive4;24" valign="top" halign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="ServiceName">Provider</convert>
    </widget>

    <widget name="subserv" position="712,949" size="0,0" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="on" />
    <widget name="wide" position="712,949" size="0,0" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="on" />
    <widget name="dolby" position="712,949" size="0,0" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="on" />
    <widget name="multi_audio" position="712,949" size="0,0" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="on" />
    <widget name="txt" position="712,949" size="0,0" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="on" />
    <widget name="hd_sd" position="1569,871" size="0,0" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="on" />
    <widget name="hbb" position="1569,871" size="0,0" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="on" />
    <widget name="subtit" position="1569,871" size="0,0" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="on" />
    <widget name="tuner" position="712,949" size="0,0" zPosition="1" alphatest="on" />
    <widget name="HDD_state" position="712,949" size="0,0" zPosition="1" alphatest="on" />    

    <widget name="Dtype" position="1768,949" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1768,949" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1768,949" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1768,949" size="0,0" zPosition="3" alphatest="off" />
 	
    <widget source="session.FrontendStatus" render="Label" font="Prive3;21" position="1449,856" zPosition="2" backgroundColor="background" size="105,24" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;21" position="1521,856" zPosition="2" backgroundColor="background" size="105,24" halign="right" transparent="1" >
    <convert type="g17ExtraSource">SnrdB</convert>
    </widget>

		<widget source="session.FrontendStatus" render="g17Ahours" position="1461,882" size="150,150" zPosition="3" foregroundColor="yellow" alphatest="on">
		<convert type="g17ExtraSource">SnrAnalog</convert>
		</widget>

		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,573"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,573"  size="150,90"  zPosition="2" alphatest="on"/>	
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />"""
g17_extraScreen["17"]  += '<ePixmap position="0,792" zPosition="-2" size="1920,333" pixmap="'+PATH+'/17/infobar4.png" alphatest="off" />\n'
g17_extraScreen["17"]  += '<ePixmap pixmap="'+PATH+'/17/snr-all.png" position="1441,849" size="192,114" zPosition="1" alphatest="off"/>\n'
g17_extraScreen["17"]  += '<ePixmap pixmap="'+PATH+'/17/snr-b.png" position="1515,940" size="46,21" zPosition="4" alphatest="off"/>\n'
g17_extraScreen["17"]  += '<widget name="back_enhanced" position="60,60"  size="465,660" pixmap="'+PATH+'/17/back_enhanced4-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["17"]  += '<widget name="caidPids_back" alphatest="off" position="1609,45"  size="255,600" pixmap="'+PATH+'/17/back_caidPids4-fs8.png" zPosition="0" />\n'
g17_extraScreen["17"]  += '<widget name="caidPids_end" alphatest="off" position="1609,115"  size="255,27" pixmap="'+PATH+'/17/end_caidPids4-fs8.png" zPosition="3" />\n'
g17_extraScreen["17"]  += """</screen>"""	

g17_extraScreen["18"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">

    <ePixmap position="73,759" size="189,123" pixmap="hd_glass17/frame_hd4.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="93,775" size="150,90" zPosition="2" transparent="1" alphatest="on" />

    <ePixmap position="1656,759" size="189,123" pixmap="hd_glass17/frame_hd4.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1675,775" size="150,90" zPosition="2" transparent="1" alphatest="on" />    
    <widget name="weaTxt" position="1675,775" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
    
  	<widget name="Video_size" font="Prive4;25" position="73,720" size="189,37" valign="top" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget position="457,711" size="780,42" source="session.CurrentService" render="Label" font="Prive4;36" valign="top" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="ServiceName">Name</convert>
    </widget>
    
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="1081,720" size="660,30" font="Prive3;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1701,720" size="135,37" font="Prive4;25" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>      
    
    <widget position="270,766" size="150,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;31" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="378,766" size="885,45" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive4;34" halign="left" valign="top" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1242,766" size="157,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;31" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget name="slider_back" position="270,817" size="1129,15" pixmap="hd_glass17/slider/slider_back4.png" zPosition="2" transparent="1" alphatest="on" />    
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main4.png" position="270,817" size="1129,15" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    
    <widget position="270,840" size="150,39" source="session.Event_Next" render="Label" font="Prive4;31" valign="top" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="378,840" size="885,45" source="session.Event_Next" render="g17EmptyEpg" font="Prive4;34" halign="left" valign="top" noWrap="1" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1242,840" size="157,39" source="session.Event_Next" render="Label" font="Prive4;31" valign="top" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" halign="right" transparent="1">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="TP_info" position="97,982" zPosition="1" size="637,34" font="Prive4;22" valign="top" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget position="1423,981" size="397,34" source="session.CurrentService" render="Label" font="Prive4;24" valign="top" halign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="ServiceName">Provider</convert>
    </widget>
    <widget name="ecmLineInfo" position="769,943" size="1066,27" font="Prive4;19" backgroundColor="background" noWrap="1" valign="top" halign="right" transparent="1" />

    <widget name="subserv" position="712,898" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="712,898" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="712,898" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="712,898" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="712,898" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="712,898" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="712,898" size="42,72" zPosition="1" alphatest="off" />    
		<widget position="712,898" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on" >
			<convert type="g17ConditionalShowHide">Blink</convert>
		</widget>
		
    <widget name="Dtype" position="1768,898" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1768,898" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1768,898" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1768,898" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1768,898" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1768,898" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1768,898" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1768,898" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1768,898" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1768,898" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1768,898" size="78,46" zPosition="3" alphatest="off" />
     	
    <widget source="session.FrontendStatus" render="Label" font="Prive3;21" position="1449,766" zPosition="2" backgroundColor="background" size="105,24" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;21" position="1521,766" zPosition="2" backgroundColor="background" size="105,24" halign="right" transparent="1" >
    <convert type="g17ExtraSource">SnrdB</convert>
    </widget>

		<widget source="session.FrontendStatus" render="g17Ahours" position="1461,792" size="150,150" zPosition="3" foregroundColor="yellow" alphatest="on">
		<convert type="g17ExtraSource">SnrAnalog</convert>
		</widget>

		<widget name="ecmlabels" font="Prive3;24" position="97,195" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="180,195" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="picProv" position="109,84"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="307,84"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="109,543"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="307,543"  size="150,90"  zPosition="2" alphatest="on"/>	
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />"""
g17_extraScreen["18"]  += '<ePixmap position="0,702" zPosition="-2" size="1920,333" pixmap="'+PATH+'/18/infobar7.png" alphatest="off" />\n'
g17_extraScreen["18"]  += '<ePixmap pixmap="'+PATH+'/18/snr-all.png" position="1441,759" size="192,114" zPosition="1" alphatest="off"/>\n'
g17_extraScreen["18"]  += '<ePixmap pixmap="'+PATH+'/18/snr-b.png" position="1515,850" size="46,21" zPosition="4" alphatest="off"/>\n'
g17_extraScreen["18"]  += '<widget name="back_enhanced" position="49,30"  size="465,660" pixmap="'+PATH+'/18/back_enhanced4-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["18"]  += '<widget name="caidPids_back" alphatest="off" position="1609,45"  size="255,600" pixmap="'+PATH+'/18/back_caidPids4-fs8.png" zPosition="0" />\n'
g17_extraScreen["18"]  += '<widget name="caidPids_end" alphatest="off" position="1609,115"  size="255,27" pixmap="'+PATH+'/18/end_caidPids4-fs8.png" zPosition="3" />\n'
g17_extraScreen["18"]  += """</screen>"""

g17_extraScreen["19"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">

    <ePixmap position="73,759" size="189,123" pixmap="hd_glass17/frame_hd4.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="93,775" size="150,90" zPosition="2" transparent="1" alphatest="on" />

    <ePixmap position="1656,759" size="189,123" pixmap="hd_glass17/frame_hd4.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1675,775" size="150,90" zPosition="2" transparent="1" alphatest="on" />    
    <widget name="weaTxt" position="1675,775" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
    
  	<widget name="Video_size" font="Prive4;25" position="73,720" size="189,37" valign="top" halign="center" foregroundColor="#000000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget position="457,711" size="780,42" source="session.CurrentService" render="Label" foregroundColor="#000000" font="Prive4;36" valign="top" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="ServiceName">Name</convert>
    </widget>
    
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="1081,720" size="660,30" font="Prive3;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1701,720" size="135,37" font="Prive4;25" foregroundColor="#000000" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>      
    
    <widget position="270,766" size="150,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;31" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="378,766" size="885,45" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive4;34" halign="left" valign="top" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1242,766" size="157,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;31" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget name="slider_back" position="270,817" size="1129,15" pixmap="hd_glass17/slider/slider_back4.png" zPosition="2" transparent="1" alphatest="on" />    
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main4.png" position="270,817" size="1129,15" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    
    <widget position="270,840" size="150,39" source="session.Event_Next" render="Label" font="Prive4;31" valign="top" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="378,840" size="885,45" source="session.Event_Next" render="g17EmptyEpg" font="Prive4;34" halign="left" valign="top" noWrap="1" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1242,840" size="157,39" source="session.Event_Next" render="Label" font="Prive4;31" valign="top" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" halign="right" transparent="1">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="TP_info" position="97,889" zPosition="1" size="637,34" font="Prive4;22" valign="top" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget position="1423,888" size="397,34" source="session.CurrentService" render="Label" font="Prive4;24" valign="top" halign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="ServiceName">Provider</convert>
    </widget>
    <widget name="ecmLineInfo" position="769,994" size="1066,27" font="Prive4;19" backgroundColor="background" noWrap="1" valign="top" halign="right" transparent="1" />

    <widget name="subserv" position="712,949" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="712,949" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="712,949" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="712,949" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="712,949" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="712,949" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="712,949" size="42,72" zPosition="1" alphatest="off" />    
		<widget position="712,949" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on" >
			<convert type="g17ConditionalShowHide">Blink</convert>
		</widget>
		
    <widget name="Dtype" position="1768,949" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1768,949" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1768,949" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1768,949" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1768,949" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1768,949" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1768,949" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1768,949" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1768,949" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1768,949" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1768,949" size="78,46" zPosition="3" alphatest="off" />
     	
    <widget source="session.FrontendStatus" render="Label" font="Prive3;21" position="1449,766" zPosition="2" backgroundColor="background" size="105,24" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;21" position="1521,766" zPosition="2" backgroundColor="background" size="105,24" halign="right" transparent="1" >
    <convert type="g17ExtraSource">SnrdB</convert>
    </widget>

		<widget source="session.FrontendStatus" render="g17Ahours" position="1461,792" size="150,150" zPosition="3" foregroundColor="yellow" alphatest="on">
		<convert type="g17ExtraSource">SnrAnalog</convert>
		</widget>

		<widget name="ecmlabels" font="Prive3;24" position="97,195" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="180,195" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="picProv" position="109,84"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="307,84"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="109,543"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="307,543"  size="150,90"  zPosition="2" alphatest="on"/>	
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />"""
g17_extraScreen["19"]  += '<ePixmap position="0,702" zPosition="-2" size="1920,333" pixmap="'+PATH+'/19/infobar6.png" alphatest="off" />\n'
g17_extraScreen["19"]  += '<ePixmap pixmap="'+PATH+'/19/snr-all.png" position="1441,762" size="192,111" zPosition="1" alphatest="off"/>\n'
g17_extraScreen["19"]  += '<ePixmap pixmap="'+PATH+'/19/snr-b.png" position="1515,850" size="46,21" zPosition="4" alphatest="off"/>\n'
g17_extraScreen["19"]  += '<widget name="caidPids_back" alphatest="off" position="1609,45"  size="255,600" pixmap="'+PATH+'/19/back_caidPids5-fs8.png" zPosition="0" />\n'
g17_extraScreen["19"]  += '<widget name="back_enhanced" position="49,30"  size="465,660" pixmap="'+PATH+'/19/back_enhanced5-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["19"]  += '<widget name="caidPids_end" alphatest="off" position="1609,115"  size="255,25" pixmap="'+PATH+'/19/end_caidPids5-fs8.png" zPosition="3" />\n'
g17_extraScreen["19"]  += """</screen>"""

g17_extraScreen["20"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">

    <ePixmap position="73,759" size="189,123" pixmap="hd_glass17/frame_hd4.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="93,775" size="150,90" zPosition="2" transparent="1" alphatest="on" />
 
    <ePixmap position="1656,759" size="189,123" pixmap="hd_glass17/frame_hd4.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1675,775" size="150,90" zPosition="2" transparent="1" alphatest="on" />    
    <widget name="weaTxt" position="1675,775" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
    
  	<widget name="Video_size" font="Prive4;25" position="73,720" size="189,37" valign="top" halign="center" foregroundColor="#000000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget position="457,711" size="780,42" source="session.CurrentService" render="Label" foregroundColor="#000000" font="Prive4;36" valign="top" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="ServiceName">Name</convert>
    </widget>
    
    <widget source="global.CurrentTime" render="g17dateFormat" foregroundColor="#000000" format="%A  %d.%B %Y" position="1081,720" size="660,37" font="Prive3;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1701,720" size="135,37" font="Prive4;25" foregroundColor="#000000" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>      
    
    <widget position="270,766" size="150,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;31" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="378,766" size="885,45" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive4;34" halign="left" valign="top" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1242,766" size="157,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;31" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget name="slider_back" position="270,817" size="1129,15" pixmap="hd_glass17/slider/slider_back4.png" zPosition="2" transparent="1" alphatest="on" />    
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main4.png" position="270,817" size="1129,15" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    
    <widget position="270,840" size="150,39" source="session.Event_Next" render="Label" font="Prive4;31" valign="top" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="378,840" size="885,45" source="session.Event_Next" render="g17EmptyEpg" font="Prive4;34" halign="left" valign="top" noWrap="1" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1242,840" size="157,39" source="session.Event_Next" render="Label" font="Prive4;31" valign="top" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" halign="right" transparent="1">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="TP_info" position="97,982" zPosition="1" size="637,34" font="Prive4;22" valign="top" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget position="1423,981" size="397,34" source="session.CurrentService" render="Label" font="Prive4;24" valign="top" halign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="ServiceName">Provider</convert>
    </widget>
    <widget name="ecmLineInfo" position="769,943" size="1066,27" font="Prive4;19" backgroundColor="background" noWrap="1" valign="top" halign="right" transparent="1" />

    <widget name="subserv" position="712,898" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="712,898" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="712,898" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="712,898" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="712,898" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="712,898" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="712,898" size="42,72" zPosition="1" alphatest="off" />    
		<widget position="712,898" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on" >
			<convert type="g17ConditionalShowHide">Blink</convert>
		</widget>
		
    <widget name="Dtype" position="1768,898" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1768,898" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1768,898" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1768,898" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1768,898" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1768,898" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1768,898" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1768,898" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1768,898" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1768,898" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1768,898" size="78,46" zPosition="3" alphatest="off" />
     	
    <widget source="session.FrontendStatus" render="Label" font="Prive3;21" position="1449,766" zPosition="2" backgroundColor="background" size="105,24" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;21" position="1521,766" zPosition="2" backgroundColor="background" size="105,24" halign="right" transparent="1" >
    <convert type="g17ExtraSource">SnrdB</convert>
    </widget>

		<widget source="session.FrontendStatus" render="g17Ahours" position="1461,792" size="150,150" zPosition="3" foregroundColor="yellow" alphatest="on">
		<convert type="g17ExtraSource">SnrAnalog</convert>
		</widget>

		<widget name="ecmlabels" font="Prive3;24" position="97,195" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="180,195" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="picProv" position="109,84"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="307,84"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="109,543"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="307,543"  size="150,90"  zPosition="2" alphatest="on"/>	
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />"""
g17_extraScreen["20"]  += '<ePixmap position="0,702" zPosition="-2" size="1920,333" pixmap="'+PATH+'/20/infobar8.png" alphatest="off" />\n'
g17_extraScreen["20"]  += '<ePixmap pixmap="'+PATH+'/20/snr-all.png" position="1441,762" size="192,111" zPosition="1" alphatest="off"/>\n'
g17_extraScreen["20"]  += '<ePixmap pixmap="'+PATH+'/20/snr-b.png" position="1515,850" size="46,21" zPosition="4" alphatest="off"/>\n'
g17_extraScreen["20"]  += '<widget name="back_enhanced" position="49,30"  size="465,660" pixmap="'+PATH+'/20/back_enhanced5-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["20"]  += '<widget name="caidPids_back" alphatest="off" position="1609,45"  size="255,600" pixmap="'+PATH+'/20/back_caidPids5-fs8.png" zPosition="0" />\n'
g17_extraScreen["20"]  += '<widget name="caidPids_end" alphatest="off" position="1609,115"  size="255,25" pixmap="'+PATH+'/20/end_caidPids5-fs8.png" zPosition="3" />\n'
g17_extraScreen["20"]  += """</screen>"""
	
g17_extraScreen["21"] = """

  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">

    <widget source="session.CurrentService" render="Label" position="285,760" size="120,39" font="Prive4;33" halign="right" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2" valign="bottom">
      <convert type="g17ServiceNum">Number</convert>
    </widget>
    <widget position="435,754" size="757,48" source="session.CurrentService" render="Label" font="Prive4;39" valign="bottom" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="ServiceName">Name</convert>
    </widget>
    <ePixmap position="120,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="960,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <widget name="TP_info" position="318,951" zPosition="1" size="750,30" font="Prive4;24" halign="left" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />
    <widget name="TP_type" position="121,952" zPosition="2" size="293,30" font="Prive4;22" halign="left" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />
    <widget name="Video_size" font="Prive4;27" position="115,766" size="180,33" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1609,754" size="135,48" font="Prive4;39" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1725,757" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="937,766" size="660,33" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="1075,826" size="525,37" font="Prive4;27" halign="right" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    
    <ePixmap position="111,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="130,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />

    <widget position="315,858" size="90,39" source="session.Event_Now" render="Label" zPosition="1" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,858" size="495,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,858" size="142,39" source="session.Event_Now" render="Label" zPosition="1" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="313,837" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="313,837" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />
    <widget position="315,892" size="90,39" source="session.Event_Next" render="Label" font="Prive4;27" transparent="1" backgroundColor="background" valign="bottom" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,892" size="495,39" source="session.Event_Next" render="g17EmptyEpg" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,892" size="142,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    <ePixmap position="1620,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1639,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />
    <widget name="weaTxt" position="1639,835" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />

    <widget name="subserv" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1569,871" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1569,871" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1569,871" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
    <widget name="ecmLineInfo" position="780,994" size="1017,24" font="Prive4;18" noWrap="1" halign="right" transparent="1" backgroundColor="background" foregroundColor="unb2e0b4" zPosition="5" />
    <eLabel text="Snr: dB" font="Prive4;24" position="121,988" size="105,30" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="226,988" size="90,30" font="Prive4;24" zPosition="5" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17ExtraSource">SnrdB</convert>
    </widget>
    <eLabel text="Snr:" position="319,988" size="60,30" font="Prive4;24" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="379,988" size="90,30" font="Prive4;24" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="469,988" size="60,30" font="Prive4;24" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="529,988" size="90,30" font="Prive4;24" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <eLabel text="Ber:" position="619,988" size="60,30" font="Prive4;24" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="679,988" size="90,30" font="Prive4;24" foregroundColor="unefb2b2" transparent="1" backgroundColor="background">
      <convert type="g17ExtraSource">BerText</convert>
    </widget>
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,571"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,571"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />"""
g17_extraScreen["21"]  += '<ePixmap position="0,736" zPosition="-2" size="1920,333" pixmap="'+PATH+'/21/infobar9-fs8.png" alphatest="off" />\n'
g17_extraScreen["21"]  += '<widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="'+PATH+'/21/back_caidPids9-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["21"]  += """<widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />    
  </screen>"""
  	
g17_extraScreen["22"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">

    <ePixmap position="81,763" size="189,123" pixmap="hd_glass17/frame_hd4.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="100,780" size="150,90" zPosition="2" transparent="1" alphatest="on" />

    <ePixmap position="1650,763" size="189,123" pixmap="hd_glass17/frame_hd4.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1669,780" size="150,90" zPosition="2" transparent="1" alphatest="on" />    
    <widget name="weaTxt" position="1669,780" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
    
  	<widget name="Video_size" font="Regular;25" position="81,726" size="189,37" valign="top" halign="center" foregroundColor="#00000000"  transparent="1" />

    <widget position="457,721" size="780,42" source="session.CurrentService" render="Label" foregroundColor="#00000000" font="Regular;36" valign="top" halign="left" noWrap="1"  transparent="1">
      <convert type="ServiceName">Name</convert>
    </widget>
    
    <widget source="global.CurrentTime" render="g17dateFormat" foregroundColor="#000000" format="%A  %d.%B %Y" position="1081,726" size="660,30" font="Regular;25" valign="top" halign="right"  transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1701,726" size="135,37" font="Regular;25" foregroundColor="#00000000" valign="top" halign="right" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>      
    
    <widget position="270,766" size="150,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;31" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="378,766" size="885,45" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive4;34" halign="left" valign="top" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1242,766" size="157,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;31" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget name="slider_back" position="270,817" size="1129,15" pixmap="hd_glass17/slider/slider_back4.png" zPosition="2" transparent="1" alphatest="on" />    
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main4.png" position="270,817" size="1129,15" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    
    <widget position="270,840" size="150,39" source="session.Event_Next" render="Label" font="Prive4;31" valign="top" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="378,840" size="885,45" source="session.Event_Next" render="g17EmptyEpg" font="Prive4;34" halign="left" valign="top" noWrap="1" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" transparent="1">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1242,840" size="157,39" source="session.Event_Next" render="Label" font="Prive4;31" valign="top" backgroundColor="#353e575e" foregroundColor="#777777" shadowOffset="-2,-1" halign="right" transparent="1">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="TP_info" position="97,982" zPosition="1" size="637,34" font="Prive4;22" valign="top" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget position="1423,981" size="397,34" source="session.CurrentService" render="Label" font="Prive4;24" valign="top" halign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="ServiceName">Provider</convert>
    </widget>
    <widget name="ecmLineInfo" position="769,946" size="1066,27" font="Prive4;19" backgroundColor="background" noWrap="1" valign="top" halign="right" transparent="1" />

    <widget name="subserv" position="712,901" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="712,901" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="712,901" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="712,901" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="712,901" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,901" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="712,901" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="712,901" size="42,72" zPosition="1" alphatest="off" />    
		<widget position="712,901" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on" >
			<convert type="g17ConditionalShowHide">Blink</convert>
		</widget>
		
    <widget name="Dtype" position="1756,901" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1756,901" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1756,901" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1756,901" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1756,901" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1756,901" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1756,901" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1756,901" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1756,901" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1756,901" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1756,901" size="78,46" zPosition="3" alphatest="off" />
     	
    <widget source="session.FrontendStatus" render="Label" font="Prive3;21" position="1449,766" zPosition="2" backgroundColor="background" size="105,24" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;21" position="1521,766" zPosition="2" backgroundColor="background" size="105,24" halign="right" transparent="1" >
    <convert type="g17ExtraSource">SnrdB</convert>
    </widget>

		<widget source="session.FrontendStatus" render="g17Ahours" position="1461,792" size="150,150" zPosition="3" foregroundColor="yellow" alphatest="on">
		<convert type="g17ExtraSource">SnrAnalog</convert>
		</widget>

		<widget name="ecmlabels" font="Prive3;24" position="97,195" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="180,195" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="picProv" position="109,84"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="307,84"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="109,543"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="307,543"  size="150,90"  zPosition="2" alphatest="on"/>	
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />"""
g17_extraScreen["22"]  += '<ePixmap position="0,702" zPosition="-2" size="1920,333" pixmap="'+PATH+'/22/infobar22-fs8.png" alphatest="off" />\n'
g17_extraScreen["22"]  += '<ePixmap pixmap="'+PATH+'/22/snr-all.png" position="1441,762" size="192,111" zPosition="1" alphatest="off"/>\n'
g17_extraScreen["22"]  += '<ePixmap pixmap="'+PATH+'/22/snr-b.png" position="1515,850" size="46,21" zPosition="4" alphatest="off"/>\n'
g17_extraScreen["22"]  += '<widget name="back_enhanced" position="49,30"  size="465,660" pixmap="'+PATH+'/22/back_enhanced22-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["22"]  += '<widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="'+PATH+'/22/back_caidPids22-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["22"]  += '<widget name="caidPids_end" position="1609,115"  size="255,48" pixmap="'+PATH+'/22/end_caidPids22-fs8.png" alphatest="off" zPosition="3" />\n'
g17_extraScreen["22"]  += """</screen>"""
	
g17_extraScreen["23"] = """

  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">

    <widget source="session.CurrentService" render="Label" position="285,760" size="120,39" font="Prive4;33" halign="right" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2" valign="bottom">
      <convert type="g17ServiceNum">Number</convert>
    </widget>
    <widget position="435,754" size="757,48" source="session.CurrentService" render="Label" font="Prive4;39" valign="bottom" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="ServiceName">Name</convert>
    </widget>
    <ePixmap position="120,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="960,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <widget name="TP_info" position="318,951" zPosition="1" size="750,30" font="Prive4;24" transparent="1" backgroundColor="background" halign="left" foregroundColor="un99bad6" />
    <widget name="TP_type" position="121,952" zPosition="2" size="293,30" font="Prive4;22" transparent="1" backgroundColor="background" halign="left" foregroundColor="un99bad6" />
    <widget name="Video_size" font="Prive4;27" position="115,766" size="180,33" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1609,754" size="135,48" font="Prive4;39" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1725,757" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="937,766" size="660,33" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="1075,826" size="525,37" font="Prive4;27" halign="right" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    
    <ePixmap position="111,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="130,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />

    <widget position="315,858" size="90,39" source="session.Event_Now" render="Label" zPosition="1" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,858" size="495,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,858" size="142,39" source="session.Event_Now" render="Label" zPosition="1" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="313,837" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="313,837" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />
    <widget position="315,892" size="90,39" source="session.Event_Next" render="Label" font="Prive4;27" transparent="1" backgroundColor="background" valign="bottom" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,892" size="495,39" source="session.Event_Next" render="g17EmptyEpg" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,892" size="142,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    <ePixmap position="1620,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1639,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />
    <widget name="weaTxt" position="1639,835" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />

    <widget name="subserv" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1569,871" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1569,871" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1569,871" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
    <widget name="ecmLineInfo" position="780,994" size="1017,24" font="Prive4;18" noWrap="1" halign="right" transparent="1" backgroundColor="background" foregroundColor="unb2e0b4" zPosition="5" />
    <eLabel text="Snr: dB" font="Prive4;24" position="121,988" size="105,30" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="226,988" size="90,30" transparent="1" backgroundColor="background" font="Prive4;24" zPosition="5" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">SnrdB</convert>
    </widget>
    <eLabel text="Snr:" position="319,988" size="60,30" font="Prive4;24" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="379,988" size="90,30" transparent="1" backgroundColor="background" font="Prive4;24" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="469,988" size="60,30" font="Prive4;24" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="529,988" size="90,30" transparent="1" backgroundColor="background" font="Prive4;24" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <eLabel text="Ber:" position="619,988" size="60,30" font="Prive4;24" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="679,988" size="90,30" transparent="1" backgroundColor="background" font="Prive4;24" foregroundColor="unefb2b2">
      <convert type="g17ExtraSource">BerText</convert>
    </widget>
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,573"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,573"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />"""
g17_extraScreen["23"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/23/infobar-exX.png" alphatest="off" />\n'
g17_extraScreen["23"]  += '<widget name="back_enhanced" position="60,60"  size="465,660" pixmap="'+PATH+'/23/back_enhancedX-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["23"]  += '<widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="'+PATH+'/23/back_caidPidsX-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["23"]  += """<widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" zPosition="3" alphatest="off" />    
  </screen>"""	

g17_extraScreen["24"] = """

    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""
g17_extraScreen["24"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/24/infobar-exX.png" alphatest="off" />\n'
g17_extraScreen["24"]  += """<widget name="Video_size" font="Prive4;27" position="100,766" size="210,33" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget source="session.CurrentService" render="Label" position="315,760" size="120,39" font="Prive4;33" halign="left" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2" valign="bottom">
      <convert type="g17ServiceNum">Number</convert>
    </widget>
    <widget position="435,754" size="757,48" source="session.CurrentService" render="Label" font="Prive4;39" valign="bottom" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="ServiceName">Name</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="937,766" size="660,33" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1609,754" size="135,48" font="Prive4;39" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1725,757" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <ePixmap position="111,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="130,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />   
  
    <widget name="Prov_temp_rpm" position="1075,826" size="525,33" font="Prive4;27" halign="right" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />

    <ePixmap position="1620,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1639,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />    
    <widget name="weaTxt" position="1639,835" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
    
    <widget position="315,828" size="90,39" source="session.Event_Now" render="Label" zPosition="1" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,828" size="495,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,828" size="142,39" source="session.Event_Now" render="Label" zPosition="1" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="313,867" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="313,867" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />    
    <widget position="315,892" size="90,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,892" size="495,39" source="session.Event_Next" render="g17EmptyEpg" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,892" size="142,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1569,871" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1569,871" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1569,871" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
    <ePixmap position="120,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="960,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <widget name="TP_type" position="121,952" zPosition="2" size="293,30" font="Prive4;22" transparent="1" backgroundColor="background" halign="left" foregroundColor="un99bad6" />
    <widget name="TP_info" position="315,951" zPosition="1" size="735,30" font="Prive4;24" transparent="1" backgroundColor="background" halign="center" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
      	
    <eLabel text="Snr:" font="Prive4;24" position="121,988" size="105,30" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="181,988" size="90,30" transparent="1" backgroundColor="background" font="Prive4;24" zPosition="5" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="271,988" size="60,30" font="Prive4;24" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="331,988" size="90,30" transparent="1" backgroundColor="background" font="Prive4;24" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <widget name="bitrate_info" position="421,988" zPosition="8" size="750,30" font="Prive3;24" halign="left" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1"/>

    <widget name="ecmLineInfo" position="780,994" size="1017,24" font="Prive4;18" noWrap="1" transparent="1" halign="right" backgroundColor="background" foregroundColor="unb2e0b4" zPosition="5" />
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,571"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,571"  size="150,90"  zPosition="2" alphatest="on"/>	
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />

	</screen>"""
	
g17_extraScreen["25"] = """

  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <ePixmap position="567,687" size="780,138" pixmap="hd_glass17/frame-chname26-fs8.png" zPosition="1" alphatest="on" />    
     <widget position="579,718" size="750,75" source="session.CurrentService" render="Label" zPosition="2" font="Prive4;45" valign="center" halign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>

    <widget name="ecmLineInfo" position="775,1002" size="1032,24" font="Prive4;18" noWrap="1" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" zPosition="5" transparent="1" />

    <widget name="TP_info" position="102,1002" zPosition="6" size="675,24" font="Prive4;21" noWrap="1" halign="left" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget name="TP_type" position="162,1002" zPosition="6" size="0,0" font="Prive4;24" halign="left" foregroundColor="un99bad6" />
    <widget name="Video_size" font="Prive4;27" position="115,766" size="0,0" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
  
		<widget source="global.CurrentTime" render="g17Ahours" position="1674,712" size="108,108" zPosition="4" alphatest="on" foregroundColor="#f23d21">
			<convert type="g17ExtraSource">secHand</convert>
		</widget>
		<widget source="global.CurrentTime" render="g17Ahours" position="1683,721" size="90,90" zPosition="3" foregroundColor="white" alphatest="on">
			<convert type="g17ExtraSource">minHand</convert>
		</widget>
		<widget source="global.CurrentTime" render="g17Ahours" position="1693,732" size="69,69" zPosition="2" foregroundColor="white" alphatest="on">
			<convert type="g17ExtraSource">hourHand</convert>
		</widget>

    <widget name="Prov_temp_rpm" position="1075,826" size="0,0" font="Prive4;27" halign="right" backgroundColor="background" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    
    <ePixmap position="118,702" size="175,138" pixmap="hd_glass17/frame25-fs8.png" zPosition="1" alphatest="on" />
    <widget name="g17picon" position="130,723" size="150,90" zPosition="2" transparent="1" alphatest="on" />
    
    <widget position="162,883" size="90,36" source="session.Event_Now" render="Label" zPosition="8" transparent="1" backgroundColor="background" font="Prive4;27" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="258,883" size="589,36" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="7" font="Prive4;27"  noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="840,883" size="142,36" source="session.Event_Now" render="Label" zPosition="6" transparent="1" backgroundColor="background" font="Prive4;27"  foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slidermain.png" position="162,967" size="837,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="162,967" size="837,21" pixmap="hd_glass17/slider/sliderback-fs8.png" zPosition="2" alphatest="on" />
 
    <widget position="162,922" size="90,30" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;27"  zPosition="8" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="258,922" size="589,30" source="session.Event_Next" render="g17EmptyEpg" transparent="1" backgroundColor="background" font="Prive4;27"  zPosition="7" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="840,922" size="142,30" source="session.Event_Next" render="Label" font="Prive4;27" transparent="1" backgroundColor="background" zPosition="6" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    
    <widget name="subserv" position="1713,882" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1713,882" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1713,882" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1713,882" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1713,882" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1713,882" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1713,882" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1713,882" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1713,882" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
		<widget name="ecmlabels" font="Prive3;24" position="108,202" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,202" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="picProv" position="120,91"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,91"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,549"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,549"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />"""

g17_extraScreen["25"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/25/infobar-25-4-fs8.png" alphatest="off" />\n'
g17_extraScreen["25"]  += '<ePixmap position="126,874" size="27,126" pixmap="'+PATH+'/25/bi-l-flat-fs8.png" zPosition="1" alphatest="on"/>\n'
g17_extraScreen["25"]  += '<ePixmap position="1761,874" size="28,126" pixmap="'+PATH+'/25/bi-r-flat-fs8.png" zPosition="1" alphatest="on"/>\n'
g17_extraScreen["25"]  += '<widget name="back_enhanced" position="60,37"  size="465,660" pixmap="'+PATH+'/25/back_enhanced25-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["25"]  += '<widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="'+PATH+'/25/back_caidPidsX-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["25"]  += '<widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="'+PATH+'/25/end_caidPids26-fs8.png" alphatest="off" zPosition="3" />\n'    
g17_extraScreen["25"]  += """</screen>"""	

g17_extraScreen["26"] = """

  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <widget source="session.FrontendStatus" render="g17Ahours" position="154,712" size="108,108" zPosition="3" foregroundColor="white" alphatest="on">
		<convert type="g17ExtraSource">SnrAnalog</convert>
		</widget>    
    <widget source="session.FrontendStatus" render="Label" font="Prive4;22" position="162,778" zPosition="4" backgroundColor="black" size="90,28" valign="center" halign="center" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <ePixmap position="567,687" size="780,138" pixmap="hd_glass17/frame-chname26-fs8.png" zPosition="1" alphatest="on" />    
    <widget position="579,718" size="750,75" source="session.CurrentService" render="Label" font="Prive4;45" zPosition="2" valign="center" halign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>

    <widget name="ecmLineInfo" position="775,1002" size="1032,24" font="Prive4;18" noWrap="1" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" zPosition="5" transparent="1" />

    <widget name="TP_info" position="102,1002" zPosition="6" size="675,24" font="Prive4;21" noWrap="1" halign="left" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget name="TP_type" position="162,1002" zPosition="6" size="0,0" font="Prive4;24" halign="left" foregroundColor="un99bad6" />
    <widget name="Video_size" font="Prive4;27" position="115,766" size="0,0" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
  
		<widget source="global.CurrentTime" render="g17Ahours" position="1674,712" size="108,108" zPosition="4" alphatest="on" foregroundColor="#f23d21">
			<convert type="g17ExtraSource">secHand</convert>
		</widget>
		<widget source="global.CurrentTime" render="g17Ahours" position="1683,721" size="90,90" zPosition="3" foregroundColor="white" alphatest="on">
			<convert type="g17ExtraSource">minHand</convert>
		</widget>
		<widget source="global.CurrentTime" render="g17Ahours" position="1693,732" size="69,69" zPosition="2" foregroundColor="white" alphatest="on">
			<convert type="g17ExtraSource">hourHand</convert>
		</widget>

    <widget name="Prov_temp_rpm" position="1075,826" size="0,0" font="Prive4;27" halign="right" backgroundColor="background" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    
    <ePixmap position="316,702" size="175,138" pixmap="hd_glass17/frame25-fs8.png" zPosition="1" alphatest="on" />
    <widget name="g17picon" position="328,723" size="150,90" zPosition="2" transparent="1" alphatest="on" />
    
    <widget position="162,883" size="90,36" source="session.Event_Now" render="Label" zPosition="8" transparent="1" backgroundColor="background" font="Prive4;27" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="258,883" size="589,36" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="7" font="Prive4;27"  noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="840,883" size="142,36" source="session.Event_Now" render="Label" zPosition="6" transparent="1" backgroundColor="background" font="Prive4;27"  foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slidermain.png" position="162,967" size="837,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="162,967" size="837,21" pixmap="hd_glass17/slider/sliderback-fs8.png" zPosition="2" alphatest="on" />
 
    <widget position="162,922" size="90,30" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;27"  zPosition="8" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="258,922" size="589,30" source="session.Event_Next" render="g17EmptyEpg" transparent="1" backgroundColor="background" font="Prive4;27"  zPosition="7" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="840,922" size="142,30" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;27"  zPosition="6" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    
    <ePixmap position="1420,702" size="175,138" pixmap="hd_glass17/frame25-fs8.png" zPosition="1" alphatest="on" />
    <widget name="picProvSat" position="1432,723" size="150,90" zPosition="2" transparent="1" alphatest="on" />
    <widget name="weaTxt" position="1432,723" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />

    <widget name="subserv" position="1713,882" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1713,882" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1713,882" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1713,882" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1713,882" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1713,882" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1713,882" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1713,882" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1713,882" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
		<widget name="ecmlabels" font="Prive3;24" position="108,202" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,202" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
     <widget name="picProv" position="120,91"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,91"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,549"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,549"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />"""
g17_extraScreen["26"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/26/infobar-26-3-fs8.png" alphatest="off" />\n'
g17_extraScreen["26"]  += '<ePixmap position="126,874" size="27,126" pixmap="'+PATH+'/26/bi-l-flat-fs8.png" zPosition="1" alphatest="on"/>\n'
g17_extraScreen["26"]  += '<ePixmap position="1761,874" size="28,126" pixmap="'+PATH+'/26/bi-r-flat-fs8.png" zPosition="1" alphatest="on"/>\n'
g17_extraScreen["26"]  += '<ePixmap position="145,703" size="127,127" pixmap="'+PATH+'/26/snrbar26-fs8.png" zPosition="-1" alphatest="on" />\n'
g17_extraScreen["26"]  += '<widget name="back_enhanced" position="60,37"  size="465,660" pixmap="'+PATH+'/26/back_enhanced25-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["26"]  += '<widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="'+PATH+'/26/back_caidPidsX-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["26"]  += '<widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="'+PATH+'/26/end_caidPids26-fs8.png" alphatest="off" zPosition="3" />\n'    
g17_extraScreen["26"]  += """</screen>"""
  
g17_extraScreen["27"] = """

  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <eLabel text="Snr:" font="Prive4;21" position="1467,729" zPosition="2" size="142,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <eLabel text="Agc:" font="Prive4;21" position="1467,759" zPosition="2" size="142,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <eLabel text="Ber:" font="Prive4;21" position="1467,789" zPosition="2" size="142,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget source="session.FrontendStatus" render="Label" font="Prive4;21" position="1519,729" zPosition="5" size="105,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive4;21" position="1519,759" zPosition="5" size="105,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" >
    <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" 	font="Prive4;21" position="1519,789" zPosition="5" size="105,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1"  >
    <convert type="g17ExtraSource">BerText</convert> 
    </widget>"""
g17_extraScreen["27"]  += '<widget source="session.FrontendStatus" render="Pixmap" pixmap="'+PATH+'/27/yellowsig27-fs8.png" position="1441,733" size="19,19" zPosition="5" alphatest="on">\n'
g17_extraScreen["27"]  += """<convert type="g17ExtraSource">SnrNum</convert>
			<convert type="ValueRange">35,67</convert>
			<convert type="ConditionalShowHide" />
    </widget>"""
g17_extraScreen["27"]  += '<widget source="session.FrontendStatus" render="Pixmap" pixmap="'+PATH+'/27/yellowsig27-fs8.png" position="1441,763" size="19,19" zPosition="5" alphatest="on">\n'
g17_extraScreen["27"]  += """<convert type="g17ExtraSource">AgcNum</convert>
			<convert type="ValueRange">35,67</convert>
			<convert type="ConditionalShowHide" />
    </widget>"""
g17_extraScreen["27"]  += '<widget source="session.FrontendStatus" render="Pixmap" pixmap="'+PATH+'/27/redsig27-fs8.png" position="1441,733" size="19,19" zPosition="5" alphatest="on">\n'
g17_extraScreen["27"]  += """<convert type="g17ExtraSource">SnrNum</convert>
			<convert type="ValueRange">1,35</convert>
			<convert type="ConditionalShowHide">Blink</convert>
    </widget>"""
g17_extraScreen["27"]  += '<widget source="session.FrontendStatus" render="Pixmap" pixmap="'+PATH+'/27/redsig27-fs8.png" position="1441,763" size="19,19" zPosition="5" alphatest="on">\n'
g17_extraScreen["27"]  += """<convert type="g17ExtraSource">AgcNum</convert>
			<convert type="ValueRange">1,35</convert>
			<convert type="ConditionalShowHide">Blink</convert>
    </widget>"""
g17_extraScreen["27"]  += '<widget source="session.FrontendStatus" render="Pixmap" pixmap="'+PATH+'/27/redsig27-fs8.png" position="1441,793" size="19,19" zPosition="5" alphatest="on">\n'
g17_extraScreen["27"]  += """<convert type="g17ExtraSource">BerNum</convert>
			<convert type="ValueRange">100,310000</convert>
			<convert type="ConditionalShowHide">Blink</convert>
    </widget>
                    
    <ePixmap position="567,687" size="780,138" pixmap="hd_glass17/frame-chname26-fs8.png" zPosition="1" alphatest="on" />    
    <widget position="579,718" size="750,75" source="session.CurrentService" render="Label" font="Prive4;45" zPosition="2" valign="center" halign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>

    <widget name="ecmLineInfo" position="775,1002" size="1032,24" font="Prive4;18" noWrap="1" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" zPosition="5" transparent="1" />

    <widget name="TP_info" position="102,1002" zPosition="6" size="675,24" font="Prive4;21" noWrap="1" halign="left" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget name="TP_type" position="162,1002" zPosition="6" size="0,0" font="Prive4;24" halign="left" foregroundColor="un99bad6" />
    <widget name="Video_size" font="Prive4;27" position="115,766" size="0,0" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
 
    <ePixmap position="1636,702" size="175,138" pixmap="hd_glass17/frame25-fs8.png" zPosition="1" alphatest="on" />  
    <widget source="global.CurrentTime" render="g17dateFormat" format="%d.%m.%Y" position="1653,780" size="142,33" font="Prive4;22" zPosition="2"  valign="center" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1645,732" size="105,40" font="Prive4;31" zPosition="2"  valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1752,735" size="60,33" font="Prive4;22" zPosition="2"  valign="top" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>

    <widget name="Prov_temp_rpm" position="1075,826" size="0,0" font="Prive4;27" halign="right" backgroundColor="background" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    
    <ePixmap position="97,702" size="175,138" pixmap="hd_glass17/frame25-fs8.png" zPosition="1" alphatest="on" />
    <widget name="g17picon" position="109,723" size="150,90" zPosition="2" transparent="1" alphatest="on" />
    
    <widget position="162,883" size="90,36" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" zPosition="8" font="Prive4;27" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="258,883" size="589,36" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="7" font="Prive4;27"  noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="840,883" size="142,36" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" zPosition="6" font="Prive4;27"  foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slidermain.png" position="162,967" size="837,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="162,967" size="837,21" pixmap="hd_glass17/slider/sliderback-fs8.png" zPosition="2" alphatest="on" />
 
    <widget position="162,922" size="90,30" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;27"  zPosition="8" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="258,922" size="589,30" source="session.Event_Next" render="g17EmptyEpg" transparent="1" backgroundColor="background" font="Prive4;27"  zPosition="7" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="840,922" size="142,30" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;27"  zPosition="6" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    
    <ePixmap position="316,702" size="175,138" pixmap="hd_glass17/frame25-fs8.png" zPosition="1" alphatest="on" />
    <widget name="picProvSat" position="328,723" size="150,90" zPosition="2" transparent="1" alphatest="on" />
    <widget name="weaTxt" position="328,723" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />

    <widget name="subserv" position="1713,882" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1713,882" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1713,882" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1713,882" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1713,882" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1713,882" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1713,882" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1713,882" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1713,882" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
		<widget name="ecmlabels" font="Prive3;24" position="108,202" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,202" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="picProv" position="120,91"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,91"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,549"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,549"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />"""

g17_extraScreen["27"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/27/infobar-27-1-fs8.png" alphatest="off" />\n'
g17_extraScreen["27"]  += '<ePixmap position="126,874" size="27,126" pixmap="'+PATH+'/27/bi-l-flat-fs8.png" zPosition="1" alphatest="on"/>\n'
g17_extraScreen["27"]  += '<ePixmap position="1761,874" size="28,126" pixmap="'+PATH+'/27/bi-r-flat-fs8.png" zPosition="1" alphatest="on"/>\n'
g17_extraScreen["27"]  += '<ePixmap position="1420,702" size="175,138" pixmap="'+PATH+'/27/sigframe27-fs8.png" zPosition="1" alphatest="on" />\n'
g17_extraScreen["27"]  += '<widget name="back_enhanced" position="60,37"  size="465,660" pixmap="'+PATH+'/27/back_enhanced25-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["27"]  += '<widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="'+PATH+'/27/back_caidPidsX-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["27"]  += '<widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="'+PATH+'/27/end_caidPids26-fs8.png" alphatest="off" zPosition="3" />\n'    
g17_extraScreen["27"]  += """</screen>"""  

g17_extraScreen["28"] = """

  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <eLabel text="Snr:" font="Prive4;21" position="1467,699" zPosition="2" size="142,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <eLabel text="Agc:" font="Prive4;21" position="1467,729" zPosition="2" size="142,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <eLabel text="Ber:" font="Prive4;21" position="1467,759" zPosition="2" size="142,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget source="session.FrontendStatus" render="Label" font="Prive4;21" position="1519,699" zPosition="5" size="105,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive4;21" position="1519,729" zPosition="5" size="105,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" >
    <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" 	font="Prive4;21" position="1519,759" zPosition="5" size="105,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1"  >
    <convert type="g17ExtraSource">BerText</convert> 
    </widget>"""
g17_extraScreen["28"]  += '<widget source="session.FrontendStatus" render="Pixmap" pixmap="'+PATH+'/28/yellowsig27-fs8.png" position="1441,703" size="19,19" zPosition="5" alphatest="on">\n'
g17_extraScreen["28"]  += """<convert type="g17ExtraSource">SnrNum</convert>
			<convert type="ValueRange">31,67</convert>
			<convert type="ConditionalShowHide" />
    </widget>"""
g17_extraScreen["28"]  += '<widget source="session.FrontendStatus" render="Pixmap" pixmap="'+PATH+'/28/yellowsig27-fs8.png" position="1441,733" size="19,19" zPosition="5" alphatest="on">\n'
g17_extraScreen["28"]  += """<convert type="g17ExtraSource">AgcNum</convert>
			<convert type="ValueRange">31,67</convert>
			<convert type="ConditionalShowHide" />
    </widget>"""
g17_extraScreen["28"]  += '<widget source="session.FrontendStatus" render="Pixmap" pixmap="'+PATH+'/28/redsig27-fs8.png" position="1441,703" size="19,19" zPosition="5" alphatest="on">\n'
g17_extraScreen["28"]  += """<convert type="g17ExtraSource">SnrNum</convert>
			<convert type="ValueRange">1,30</convert>
			<convert type="ConditionalShowHide">Blink</convert>
    </widget>"""
g17_extraScreen["28"]  += '<widget source="session.FrontendStatus" render="Pixmap" pixmap="'+PATH+'/28/redsig27-fs8.png" position="1441,733" size="19,19" zPosition="5" alphatest="on">\n'
g17_extraScreen["28"]  += """<convert type="g17ExtraSource">AgcNum</convert>
			<convert type="ValueRange">1,30</convert>
			<convert type="ConditionalShowHide">Blink</convert>
    </widget>"""
g17_extraScreen["28"]  += '<widget source="session.FrontendStatus" render="Pixmap" pixmap="'+PATH+'/28/redsig27-fs8.png" position="1441,763" size="19,19" zPosition="5" alphatest="on">\n'
g17_extraScreen["28"]  += """<convert type="g17ExtraSource">BerNum</convert>
			<convert type="ValueRange">100,310000</convert>
			<convert type="ConditionalShowHide">Blink</convert>
    </widget>"""
                    
g17_extraScreen["28"]  += '<ePixmap position="567,610" size="780,115" pixmap="'+PATH+'/28/frame-chname26-small-fs8.png" zPosition="1" alphatest="on" />\n'    
g17_extraScreen["28"]  += """<widget position="579,642" size="750,52" source="session.CurrentService" render="Label" font="Prive4;42" zPosition="2" valign="center" halign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
   
    <widget name="bitrate_info" position="64,1017" zPosition="6" size="525,24" font="Prive4;19" noWrap="1" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" />
    <widget name="ecmLineInfo" position="813,1017" size="1032,24" font="Prive4;18" noWrap="1" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" zPosition="5" transparent="1" />

    <widget name="TP_info" position="691,759" zPosition="6" size="675,39" font="Prive4;21" noWrap="1" halign="right" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget name="TP_type" position="546,759" zPosition="7" size="257,39" font="Prive4;21" halign="left" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget name="Video_size" font="Prive4;27" position="115,766" size="0,0" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
 
    <ePixmap position="1636,672" size="175,138" pixmap="hd_glass17/frame25-fs8.png" zPosition="1" alphatest="on" />  
    <widget source="global.CurrentTime" render="g17dateFormat" format="%d.%m.%Y" position="1653,750" size="142,33" font="Prive4;22" zPosition="2"  valign="center" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1645,702" size="105,40" font="Prive4;31" zPosition="2"  valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1752,705" size="60,33" font="Prive4;22" zPosition="2"  valign="top" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>

    <widget name="Prov_temp_rpm" position="420,1017" size="408,24" font="Prive4;19" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" zPosition="5" transparent="1"  />

    <widget name="Dtype" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    
    <ePixmap position="97,672" size="175,138" pixmap="hd_glass17/frame25-fs8.png" zPosition="1" alphatest="on" />
    <widget name="g17picon" position="109,693" size="150,90" zPosition="2" transparent="1" alphatest="on" />
    
    <widget position="162,846" size="120,57" source="session.Event_Now" transparent="1" backgroundColor="background" valign="center" render="Label" zPosition="8" font="Prive4;33" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="288,846" size="567,57" source="session.Event_Now" transparent="1" backgroundColor="background" valign="center" render="g17EmptyEpg" readTagInfo="1" zPosition="7" font="Prive4;34"  noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="855,846" size="157,57" source="session.Event_Now" transparent="1" backgroundColor="background" valign="center" render="Label" zPosition="6" font="Prive4;31"  foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slidermain.png" position="177,900" size="837,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="177,900" size="837,21" pixmap="hd_glass17/slider/sliderback-fs8.png" zPosition="2" alphatest="on" />
 
    <widget position="162,925" size="120,45" source="session.Event_Next" transparent="1" backgroundColor="background" valign="center" render="Label" font="Prive4;33"  zPosition="8" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="288,925" size="582,45" source="session.Event_Next" transparent="1" backgroundColor="background" valign="center" render="g17EmptyEpg" font="Prive4;34"  zPosition="7" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="870,925" size="142,45" source="session.Event_Next" transparent="1" backgroundColor="background" valign="center" render="Label" font="Prive4;31"  zPosition="6" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    
    <ePixmap position="316,672" size="175,138" pixmap="hd_glass17/frame25-fs8.png" zPosition="1" alphatest="on" />
    <widget name="picProvSat" position="328,693" size="150,90" zPosition="2" transparent="1" alphatest="on" />
    <widget name="weaTxt" position="328,693" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />

    <widget name="subserv" position="1713,852" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1713,852" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1713,852" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1713,852" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1713,852" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1713,852" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1713,852" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1713,852" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1713,852" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
		<widget name="ecmlabels" font="Prive3;24" position="108,172" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,172" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="picProv" position="120,61"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,61"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,519"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,519"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />"""

g17_extraScreen["28"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/28/infobar-28-2-fs8.png" alphatest="off" />\n'
g17_extraScreen["28"]  += '<ePixmap position="126,844" size="27,126" pixmap="'+PATH+'/28/bi-l-flat-fs8.png" zPosition="1" alphatest="on"/>\n'
g17_extraScreen["28"]  += '<ePixmap position="1761,844" size="28,126" pixmap="'+PATH+'/28/bi-r-flat-fs8.png" zPosition="1" alphatest="on"/>\n'
g17_extraScreen["28"]  += '<ePixmap position="1420,672" size="175,138" pixmap="'+PATH+'/28/sigframe27-fs8.png" zPosition="1" alphatest="on" />\n' 
g17_extraScreen["28"]  += '<widget name="back_enhanced" position="60,7"  size="465,660" pixmap="'+PATH+'/28/back_enhanced25-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["28"]  += '<widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="'+PATH+'/28/back_caidPidsX-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["28"]  += '<widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="'+PATH+'/28/end_caidPids26-fs8.png" alphatest="off" zPosition="3" />\n'    
g17_extraScreen["28"]  += """</screen>""" 

g17_extraScreen["29"] = """

    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <eLabel text="Snr:" font="Prive4;21" position="1467,699" zPosition="2" size="142,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <eLabel text="Agc:" font="Prive4;21" position="1467,729" zPosition="2" size="142,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <eLabel text="Ber:" font="Prive4;21" position="1467,759" zPosition="2" size="142,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget source="session.FrontendStatus" render="Label" font="Prive4;21" position="1519,699" zPosition="5" size="105,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive4;21" position="1519,729" zPosition="5" size="105,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" >
    <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" 	font="Prive4;21" position="1519,759" zPosition="5" size="105,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1"  >
    <convert type="g17ExtraSource">BerText</convert> 
    </widget>"""
g17_extraScreen["29"]  += '<widget source="session.FrontendStatus" render="Pixmap" pixmap="'+PATH+'/29/yellowsig27-fs8.png" position="1441,703" size="19,19" zPosition="5" alphatest="blend">\n'
g17_extraScreen["29"]  += """<convert type="g17ExtraSource">SnrNum</convert>
			<convert type="ValueRange">31,67</convert>
			<convert type="ConditionalShowHide" />
    </widget>"""
g17_extraScreen["29"]  += '<widget source="session.FrontendStatus" render="Pixmap" pixmap="'+PATH+'/29/yellowsig27-fs8.png" position="1441,733" size="19,19" zPosition="5" alphatest="blend">\n'
g17_extraScreen["29"]  += """<convert type="g17ExtraSource">AgcNum</convert>
			<convert type="ValueRange">31,67</convert>
			<convert type="ConditionalShowHide" />
    </widget>"""
g17_extraScreen["29"]  += '<widget source="session.FrontendStatus" render="Pixmap" pixmap="'+PATH+'/29/redsig27-fs8.png" position="1441,703" size="19,19" zPosition="5" alphatest="blend">\n'
g17_extraScreen["29"]  += """<convert type="g17ExtraSource">SnrNum</convert>
			<convert type="ValueRange">1,30</convert>
			<convert type="ConditionalShowHide">Blink</convert>
    </widget>"""
g17_extraScreen["29"]  += '<widget source="session.FrontendStatus" render="Pixmap" pixmap="'+PATH+'/29/redsig27-fs8.png" position="1441,733" size="19,19" zPosition="5" alphatest="blend">\n'
g17_extraScreen["29"]  += """<convert type="g17ExtraSource">AgcNum</convert>
			<convert type="ValueRange">1,30</convert>
			<convert type="ConditionalShowHide">Blink</convert>
    </widget>"""
g17_extraScreen["29"]  += '<widget source="session.FrontendStatus" render="Pixmap" pixmap="'+PATH+'/29/redsig27-fs8.png" position="1441,763" size="19,19" zPosition="5" alphatest="blend">\n'
g17_extraScreen["29"]  += """<convert type="g17ExtraSource">BerNum</convert>
			<convert type="ValueRange">100,310000</convert>
			<convert type="ConditionalShowHide">Blink</convert>
    </widget>"""
                    
g17_extraScreen["29"]  += '<ePixmap position="567,610" size="780,115" pixmap="'+PATH+'/29/frame-chname26-small-fs8.png" zPosition="1" alphatest="on" />\n'    
g17_extraScreen["29"]  += """<widget position="579,642" size="750,52" source="session.CurrentService" render="Label" font="Prive4;42" zPosition="2" valign="center" halign="center" noWrap="1" foregroundColor="#00ff8000" backgroundColor="un353e575e" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
   
    <widget name="bitrate_info" position="771,795" zPosition="6" size="597,33" font="Prive4;24" noWrap="1" valign="center" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" />
    <widget name="ecmLineInfo" position="663,1017" size="1182,24" font="Prive4;21" noWrap="1" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" zPosition="5" transparent="1" />

    <widget name="TP_info" position="537,757" zPosition="6" size="840,34" font="Prive4;24" noWrap="1" halign="center" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget name="TP_type" position="546,795" zPosition="6" size="225,33" font="Prive4;24" halign="left" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget name="Video_size" font="Prive4;24" position="735,795" size="225,33" zPosition="6" halign="center" valign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
 
    <ePixmap position="1636,672" size="175,138" pixmap="hd_glass17/frame25-fs8.png" zPosition="1" alphatest="on" />  
    <widget source="global.CurrentTime" render="g17dateFormat" format="%d.%m.%Y" position="1653,750" size="142,33" font="Prive4;22" zPosition="2"  valign="center" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1645,702" size="105,40" font="Prive4;31" zPosition="2"  valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1752,705" size="60,33" font="Prive4;22" zPosition="2"  valign="top" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>

    <widget name="Prov_temp_rpm" position="64,1017" size="603,24" font="Prive4;22" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" zPosition="5" transparent="1"  />

    <widget name="Dtype" position="1690,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1690,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1690,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1690,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1690,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1690,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1690,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1690,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1690,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1690,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1690,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1690,924" size="78,46" zPosition="3" alphatest="off" />
    
     <ePixmap position="97,672" size="175,138" pixmap="hd_glass17/frame25-fs8.png" zPosition="1" alphatest="on" />
    <widget name="g17picon" position="109,693" size="150,90" zPosition="2" transparent="1" alphatest="on" />
    
    <widget position="153,846" size="120,57" source="session.Event_Now" transparent="1" backgroundColor="background" valign="center" render="Label" zPosition="8" font="Prive4;33" foregroundColor="#00ff8000">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="279,846" size="552,57" source="session.Event_Now" transparent="1" backgroundColor="background" valign="center" render="g17EmptyEpg" readTagInfo="1" zPosition="7" font="Prive4;34"  noWrap="1" foregroundColor="#00ff8000">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="831,846" size="157,57" source="session.Event_Now" transparent="1" backgroundColor="background" valign="center" render="Label" zPosition="6" font="Prive4;31"  foregroundColor="#00ff8000" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slidermain.png" position="168,900" size="837,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="168,900" size="837,21" pixmap="hd_glass17/slider/sliderback-fs8.png" zPosition="2" alphatest="on" />
 
    <widget position="153,925" size="120,45" source="session.Event_Next" transparent="1" backgroundColor="background" valign="center" render="Label" font="Prive4;33"  zPosition="8" foregroundColor="#0000ff00">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="279,925" size="567,45" source="session.Event_Next" transparent="1" backgroundColor="background" valign="center" render="g17EmptyEpg" font="Prive4;34"  zPosition="7" noWrap="1" foregroundColor="#0000ff00">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="816,925" size="157,45" source="session.Event_Next" transparent="1" backgroundColor="background" valign="center" render="Label" font="Prive4;31"  zPosition="6" foregroundColor="#0000ff00" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    <widget source="session.FrontendInfo" render="g17TunersLabel" font="Regular2;28" alphatest="off" position="1002,862" size="217,61" tuners="5" ActiveTunerColor="#0000d100" backgroundColor="background" BackgroundActiveTunerColor="#00ecb100" zPosition="2"/>
    
    <ePixmap position="316,672" size="175,138" pixmap="hd_glass17/frame25-fs8.png" zPosition="1" alphatest="on" />
    <widget name="picProvSat" position="328,693" size="150,90" zPosition="2" transparent="1" alphatest="on" />
    <widget name="weaTxt" position="328,693" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />

    <widget name="subserv" position="1728,852" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1728,852" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1728,852" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1728,852" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1728,852" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1728,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1728,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1728,852" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1728,852" size="0,0" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1728,852" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1728,852" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>    
		<widget name="ecmlabels" font="Prive3;24" position="108,172" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,172" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="picProv" position="120,61"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,61"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,519"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,519"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />"""

g17_extraScreen["29"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/29/infobar-29-2-fs8.png" alphatest="off" />\n'
g17_extraScreen["29"]  += '<ePixmap position="126,844" size="27,126" pixmap="'+PATH+'/29/bi-l-flat-fs8.png" zPosition="-1" alphatest="on"/>\n'
g17_extraScreen["29"]  += '<ePixmap position="1761,844" size="28,126" pixmap="'+PATH+'/29/bi-r-flat-fs8.png" zPosition="-1" alphatest="on"/>\n'
g17_extraScreen["29"]  += '<ePixmap position="1420,672" size="175,138" pixmap="'+PATH+'/29/sigframe27-fs8.png" zPosition="1" alphatest="on" />\n' 
g17_extraScreen["29"]  += '<widget name="back_enhanced" position="60,7"  size="465,660" pixmap="'+PATH+'/29/back_enhanced25-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["29"]  += '<widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="'+PATH+'/29/back_caidPidsX-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["29"]  += '<widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="'+PATH+'/29/end_caidPids26-fs8.png" alphatest="off" zPosition="3" />\n'    
g17_extraScreen["29"]  += """</screen>"""
  
g17_extraScreen["30"] = """

    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <widget position="579,642" size="750,52" source="session.CurrentService" render="Label" font="Prive4;42" zPosition="2" valign="center" halign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
   
    <widget name="bitrate_info" position="771,795" zPosition="6" size="597,33" font="Prive4;24" noWrap="1" valign="center" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" />
    <widget name="ecmLineInfo" position="663,1017" size="1182,24" font="Prive4;21" noWrap="1" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" zPosition="5" transparent="1" />

    <widget name="TP_info" position="537,757" zPosition="6" size="840,34" font="Prive4;24" noWrap="1" halign="center" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget name="TP_type" position="546,795" zPosition="6" size="225,33" font="Prive4;24" halign="left" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget name="Video_size" font="Prive4;24" position="735,795" size="225,33" zPosition="6" halign="center" valign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
 
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="1435,799" size="373,30" font="Prive4;22" valign="center" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget source="session.FrontendStatus" render="g17Ahours" position="1480,661" size="108,108" zPosition="3" foregroundColor="white" alphatest="on">
		<convert type="g17ExtraSource">SnrAnalog</convert>
		</widget>    
    <widget source="session.FrontendStatus" render="Label" font="Prive4;22" position="1488,727" zPosition="4" backgroundColor="black" size="90,28" valign="center" halign="center" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
  
		<widget source="global.CurrentTime" render="g17Ahours" position="1654,661" size="108,108" zPosition="4" alphatest="on" foregroundColor="#f23d21">
			<convert type="g17ExtraSource">secHand</convert>
		</widget>
		<widget source="global.CurrentTime" render="g17Ahours" position="1663,670" size="90,90" zPosition="3" foregroundColor="white" alphatest="on">
			<convert type="g17ExtraSource">minHand</convert>
		</widget>
		<widget source="global.CurrentTime" render="g17Ahours" position="1674,681" size="69,69" zPosition="2" foregroundColor="white" alphatest="on">
			<convert type="g17ExtraSource">hourHand</convert>
		</widget>

    <widget name="Prov_temp_rpm" position="64,1017" size="603,24" font="Prive4;22" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" zPosition="5" transparent="1"  />

    <widget name="Dtype" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    
     <ePixmap position="97,672" size="175,138" pixmap="hd_glass17/frame25-fs8.png" zPosition="1" alphatest="on" />
    <widget name="g17picon" position="109,693" size="150,90" zPosition="2" transparent="1" alphatest="on" />
    
    <widget position="162,846" size="120,57" source="session.Event_Now" transparent="1" backgroundColor="background" valign="center" render="Label" zPosition="8" font="Prive4;33" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="288,846" size="567,57" source="session.Event_Now" transparent="1" backgroundColor="background" valign="center" render="g17EmptyEpg" readTagInfo="1" zPosition="7" font="Prive4;34"  noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="855,846" size="157,57" source="session.Event_Now" transparent="1" backgroundColor="background" valign="center" render="Label" zPosition="6" font="Prive4;31"  foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slidermain.png" position="177,900" size="837,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="177,900" size="837,21" pixmap="hd_glass17/slider/sliderback-fs8.png" zPosition="2" alphatest="on" />
 
    <widget position="162,925" size="120,45" source="session.Event_Next" transparent="1" backgroundColor="background" valign="center" render="Label" font="Prive4;33"  zPosition="8" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="288,925" size="582,45" source="session.Event_Next" transparent="1" backgroundColor="background" valign="center" render="g17EmptyEpg" font="Prive4;34"  zPosition="7" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="870,925" size="142,45" source="session.Event_Next" transparent="1" backgroundColor="background" valign="center" render="Label" font="Prive4;31"  zPosition="6" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    
    <ePixmap position="316,672" size="175,138" pixmap="hd_glass17/frame25-fs8.png" zPosition="1" alphatest="on" />
    <widget name="picProvSat" position="328,693" size="150,90" zPosition="2" transparent="1" alphatest="on" />
    <widget name="weaTxt" position="328,693" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />

    <widget name="subserv" position="1713,852" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1713,852" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1713,852" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1713,852" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1713,852" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1713,852" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1713,852" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1713,852" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1713,852" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
		<widget name="ecmlabels" font="Prive3;24" position="108,172" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,172" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="picProv" position="120,61"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,61"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,519"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,519"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />"""

g17_extraScreen["30"]  += '<ePixmap position="567,610" size="780,115" pixmap="'+PATH+'/30/frame-chname26-small-fs8.png" zPosition="1" alphatest="on" />\n'    
g17_extraScreen["30"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/30/infobar-30-fs8.png" alphatest="off" />\n'
g17_extraScreen["30"]  += '<ePixmap position="126,844" size="27,126" pixmap="'+PATH+'/30/bi-l-flat-fs8.png" zPosition="1" alphatest="on"/>\n'
g17_extraScreen["30"]  += '<ePixmap position="1761,844" size="28,126" pixmap="'+PATH+'/30/bi-r-flat-fs8.png" zPosition="1" alphatest="on"/>\n'
g17_extraScreen["30"]  += '<ePixmap position="1471,652" size="127,127" pixmap="'+PATH+'/30/sig-30-fs8.png" zPosition="1" alphatest="on" />\n' 
g17_extraScreen["30"]  += '<widget name="back_enhanced" position="60,7"  size="465,660" pixmap="'+PATH+'/30/back_enhanced25-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["30"]  += '<widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="'+PATH+'/30/back_caidPidsX-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["30"]  += '<widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="'+PATH+'/30/end_caidPids26-fs8.png" alphatest="off" zPosition="3" />\n'    
g17_extraScreen["30"]  += """</screen>"""    

g17_extraScreen["31"] = """

    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""
g17_extraScreen["31"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/31/infobar-exX-fs8.png" />\n'
g17_extraScreen["31"]  += '<widget name="back_enhanced" position="60,36"  size="465,684" pixmap="'+PATH+'/31/back_enhanced-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["31"]  += '<widget name="caidPids_end" position="1609,115"  size="255,46" pixmap="'+PATH+'/31/end_caidPids-fs8.png" alphatest="off" zPosition="3" />\n'
g17_extraScreen["31"]  += '<widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="'+PATH+'/31/back_caidPids-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["31"]  += """<widget name="Video_size" font="Prive4;27" position="100,774" size="210,33" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget source="session.CurrentService" render="Label" position="315,768" size="120,39" font="Prive4;33" halign="left" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2" valign="bottom">
      <convert type="g17ServiceNum">Number</convert>
    </widget>
    <widget position="435,762" size="757,48" source="session.CurrentService" render="Label" font="Prive4;39" valign="bottom" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="ServiceName">Name</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="937,774" size="660,30" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1609,762" size="135,48" font="Prive4;39" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1725,765" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <ePixmap position="111,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="130,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />   
  
    <widget name="Prov_temp_rpm" position="1075,826" size="525,33" font="Prive4;27" halign="right" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" />

    <ePixmap position="1620,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1639,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />    
    <widget name="weaTxt" position="1639,835" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
    
    <widget position="315,828" size="90,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,828" size="495,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,828" size="142,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="313,867" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="313,867" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />    
    <widget position="315,892" size="90,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,892" size="495,39" source="session.Event_Next" render="g17EmptyEpg" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,892" size="142,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" backgroundColor="black" alphatest="blend" />
    <widget name="wide" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" backgroundColor="black" alphatest="blend" />
    <widget name="dolby" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" backgroundColor="black" alphatest="blend" />
    <widget name="multi_audio" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" backgroundColor="black" alphatest="blend" />
    <widget name="txt" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" backgroundColor="black" alphatest="blend" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="on" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="blend" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" backgroundColor="black" alphatest="blend" />
    <widget name="tuner" position="1569,871" size="42,72" zPosition="1" backgroundColor="black" alphatest="blend" />
    <widget name="HDD_state" position="1569,871" size="42,72" zPosition="1" backgroundColor="black" alphatest="blend" />    
    <widget position="1569,871" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" backgroundColor="black" alphatest="blend">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
    <ePixmap position="120,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="960,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <widget name="TP_type" position="121,952" zPosition="2" size="293,30" font="Prive4;22" halign="left" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" />
    <widget name="TP_info" position="315,951" zPosition="1" size="735,30" font="Prive4;24" halign="center" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" />

    <widget name="Dtype" position="1723,951" size="78,46" zPosition="3" backgroundColor="black" alphatest="blend" />
    <widget name="Dcam" position="1723,951" size="78,46" zPosition="3" backgroundColor="black" alphatest="blend" />
    <widget name="Decm" position="1723,951" size="78,46" zPosition="3" backgroundColor="black" alphatest="blend" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" backgroundColor="black" alphatest="blend" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="blend" />
      	
    <eLabel text="Snr:" font="Prive4;24" position="121,988" size="105,30" foregroundColor="un99bad6" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" />
    <widget source="session.FrontendStatus" render="Label" position="181,988" size="90,30" font="Prive4;24" zPosition="5" foregroundColor="unb2e0b4" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="271,988" size="60,30" font="Prive4;24" foregroundColor="un99bad6" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" />
    <widget source="session.FrontendStatus" render="Label" position="331,988" size="90,30" font="Prive4;24" foregroundColor="unb2e0b4" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <widget name="bitrate_info" position="421,988" zPosition="8" size="750,30" font="Prive3;24" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1"/>

    <widget name="ecmLineInfo" position="780,994" size="1017,24" font="Prive4;18" noWrap="1" halign="right" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" foregroundColor="unb2e0b4" zPosition="5" />
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,573"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,573"  size="150,90"  zPosition="2" alphatest="on"/>	
    <widget name="caidPids" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="active_caidPid" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />

	</screen>"""
	
g17_extraScreen["32"] = """

    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""
g17_extraScreen["32"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/32/infobar-exX-fs8.png" alphatest="off" />\n'
g17_extraScreen["32"]  += '<widget name="back_enhanced" position="60,36"  size="465,684" pixmap="'+PATH+'/32/back_enhanced-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["32"]  += '<widget name="caidPids_end" position="1609,115"  size="255,46" pixmap="'+PATH+'/32/end_caidPids-fs8.png" alphatest="off" zPosition="3" />\n'
g17_extraScreen["32"]  += '<widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="'+PATH+'/32/back_caidPids-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["32"]  += """<widget name="Video_size" font="Prive4;27" position="132,781" size="187,46" halign="center" foregroundColor="black" backgroundColor="white" shadowColor="white" shadowOffset="-1,0" transparent="1" />

    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="991,774" size="660,30" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1659,768" size="135,48" font="Prive4;39" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1797,772" size="69,33" font="Prive4;27" valign="top" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <ePixmap position="130,841" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="150,858" size="150,90" zPosition="2" transparent="1" alphatest="on" />    
  
    <widget name="Prov_temp_rpm" position="1075,826" size="0,0" font="Prive4;27" halign="right" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" />

    <widget position="397,768" size="750,52" source="session.CurrentService" render="Label" font="Prive4;42" zPosition="2" valign="center" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
        
    <widget position="397,865" size="90,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;28" valign="bottom" foregroundColor="unb2e0b4" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="519,865" size="586,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive4;28" valign="bottom" noWrap="1" foregroundColor="unb2e0b4" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1074,865" size="142,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;28" valign="bottom" foregroundColor="unb2e0b4" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="439,832" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="439,832" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />    
    <widget position="397,916" size="90,39" source="session.Event_Next" render="Label" font="Prive4;28" valign="bottom" foregroundColor="un99bad6" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="519,916" size="586,39" source="session.Event_Next" render="g17EmptyEpg" font="Prive4;28" valign="bottom" noWrap="1" foregroundColor="un99bad6" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1074,916" size="142,39" source="session.Event_Next" render="Label" font="Prive4;28" valign="bottom" foregroundColor="un99bad6" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1803,880" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" backgroundColor="black" alphatest="blend" />
    <widget name="wide" position="1803,880" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" backgroundColor="black" alphatest="blend" />
    <widget name="dolby" position="1803,880" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" backgroundColor="black" alphatest="blend" />
    <widget name="multi_audio" position="1803,880" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" backgroundColor="black" alphatest="blend" />
    <widget name="txt" position="1803,880" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" backgroundColor="black" alphatest="blend" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="on" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="on" />
    <widget name="subtit" position="1803,880" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" backgroundColor="black" alphatest="blend" />
    <widget name="tuner" position="1803,880" size="42,72" zPosition="1" backgroundColor="black" alphatest="blend" />
    <widget name="HDD_state" position="1803,880" size="42,72" zPosition="1" backgroundColor="black" alphatest="blend" />    
    <widget position="1803,880" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" backgroundColor="black" alphatest="blend">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
    <ePixmap position="379,966" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="1014,966" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <widget name="TP_type" position="121,951" zPosition="1" size="0,0" font="Prive4;24" halign="left" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" />
    <widget name="TP_info" position="397,988" zPosition="1" size="735,30" font="Prive4;24" halign="left" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" />

    <widget name="Dtype" position="1765,981" size="78,46" zPosition="3" backgroundColor="black" alphatest="blend" />
    <widget name="Dcam" position="1765,981" size="78,46" zPosition="3" backgroundColor="black" alphatest="blend" />
    <widget name="Decm" position="1765,981" size="78,46" zPosition="3" backgroundColor="black" alphatest="blend" />
    <widget name="Dnetstate" position="1765,981" size="78,46" zPosition="3" backgroundColor="black" alphatest="blend" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1765,981" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1765,981" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1765,981" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1765,981" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1765,981" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1765,981" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1765,981" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1765,981" size="78,46" zPosition="3" alphatest="blend" />
      	
    <eLabel text="Q:" font="Prive4;27" position="100,985" size="105,30" zPosition="1"  foregroundColor="black" backgroundColor="white" shadowColor="white" shadowOffset="-1,0" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="138,985" size="90,30" halign="left" font="Prive4;27" zPosition="2"  foregroundColor="black" backgroundColor="white" shadowColor="white" shadowOffset="-1,0" transparent="1">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="S:" position="243,985" size="60,30" font="Prive4;27" zPosition="3" foregroundColor="black" backgroundColor="white" shadowColor="white" shadowOffset="-1,0" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="279,985" size="90,30" font="Prive4;27" halign="left" zPosition="4"  foregroundColor="black" backgroundColor="white" shadowColor="white" shadowOffset="-1,0" transparent="1">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <widget name="bitrate_info" position="1243,826" zPosition="8" size="600,30" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1"/>

    <widget name="ecmLineInfo" position="780,994" size="0,0" font="Prive4;18" noWrap="1" halign="right" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" foregroundColor="unb2e0b4" zPosition="5" />
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,573"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,573"  size="150,90"  zPosition="2" alphatest="on"/>	
    <widget name="caidPids" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="active_caidPid" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />

	</screen>"""	

g17_extraScreen["33"] = """
        <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
        <eLabel text="SNR:" font="Prive4;27" position="1437,708" zPosition="2" size="142,37" halign="center" backgroundColor="#00000000" foregroundColor="#00ffffff" transparent="1" />

        <widget source="session.FrontendStatus" render="Label" font="Prive4;27" position="1420,744" zPosition="5" size="175,45" halign="center" backgroundColor="#00000000" foregroundColor="#00ffffff" transparent="1" >
        <convert type="g17ExtraSource">SnrdB2</convert>
        </widget>"""                      
g17_extraScreen["33"]  += '<ePixmap position="567,610" size="780,115" pixmap="'+PATH+'/33/frame-chname26-small-fs8.png" zPosition="1" alphatest="on" />\n'  
g17_extraScreen["33"]  += """<widget position="579,642" size="750,52" source="session.CurrentService" render="Label" font="Prive4;42" zPosition="2" valign="center" halign="center" noWrap="1" foregroundColor="#00ff8000" backgroundColor="#00000000" transparent="1">
          <convert type="g17ServiceNum">NumberAndName</convert>
        </widget>
      
        <widget name="bitrate_info" position="771,795" zPosition="6" size="597,33" font="Prive4;24" noWrap="1" valign="center" halign="right" backgroundColor="#00000000" transparent="1" />
        <widget name="ecmLineInfo" position="663,1017" size="1182,24" font="Prive4;21" noWrap="1" halign="right" backgroundColor="#00000000" zPosition="5" />

        <widget name="TP_info" position="555,757" zPosition="6" size="645,33" font="Prive4;24" noWrap="1" halign="left" valign="center" backgroundColor="#00000000" transparent="1" />
        <widget name="TP_type" position="900,757" zPosition="6" size="468,33" font="Prive4;24" noWrap="1" halign="right" valign="center" backgroundColor="#00000000" transparent="1" />
        <widget name="Video_size" font="Prive4;24" position="555,795" size="502,30" zPosition="6" halign="left" valign="center" backgroundColor="#00000000" transparent="1" />
    
        <ePixmap position="1636,672" size="175,138" pixmap="hd_glass17/frame25-fs8.png" zPosition="1" alphatest="on" />
        <ePixmap position="1420,672" size="175,138" pixmap="hd_glass17/frame25-fs8.png" zPosition="1" alphatest="on" />
        <widget source="global.CurrentTime" render="g17dateFormat" foregroundColor="#00ffffff" format="%d.%m.%Y" position="1653,750" size="142,33" font="Prive4;22" zPosition="2"  valign="center" halign="center" backgroundColor="#00000000" transparent="1" />
        <widget source="global.CurrentTime" render="Label" position="1645,702" size="105,40" font="Prive4;31" zPosition="2"  valign="top" halign="right" backgroundColor="#00000000" foregroundColor="#00ffffff" transparent="1">
          <convert type="g17ClockToText">Default</convert>
        </widget>
        <widget source="global.CurrentTime" render="Label" position="1752,705" size="60,33" font="Prive4;22" zPosition="2"  valign="top" halign="left" backgroundColor="#00000000" foregroundColor="#00ffffff" transparent="1">
          <convert type="g17ClockToText">Format::%S</convert>
        </widget>
        <widget name="Prov_temp_rpm" position="64,1017" size="603,24" font="Prive4;22" halign="left" backgroundColor="#00000000" zPosition="5" transparent="1"  />
        <widget name="Dtype" position="1690,924" size="78,46" zPosition="3" alphatest="blend" />
        <widget name="Dcam" position="1690,924" size="78,46" zPosition="3" alphatest="blend" />
        <widget name="Decm" position="1690,924" size="78,46" zPosition="3" alphatest="blend" />
        <widget name="Dnetstate" position="1690,951" size="78,46" zPosition="3" alphatest="blend" />
        <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1690,924" size="78,46" zPosition="3" alphatest="blend" />
        <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1690,924" size="78,46" zPosition="3" alphatest="blend" />
        <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1690,924" size="78,46" zPosition="3" alphatest="blend" />
        <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1690,924" size="78,46" zPosition="3" alphatest="blend" />
        <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1690,924" size="78,46" zPosition="3" alphatest="blend" />
        <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1690,924" size="78,46" zPosition="3" alphatest="blend" />
        <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1690,924" size="78,46" zPosition="3" alphatest="blend" />
        <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1690,924" size="78,46" zPosition="3" alphatest="blend" />
    
           <ePixmap position="97,672" size="175,138" pixmap="hd_glass17/frame25-fs8.png" zPosition="1" alphatest="on" />
        <widget name="g17picon" position="109,693" size="150,90" zPosition="2" transparent="1" alphatest="on" />
      
        <widget position="153,846" size="120,57" source="session.Event_Now" transparent="1" backgroundColor="#00000000" valign="center" render="Label" zPosition="8" font="Prive4;33" foregroundColor="#00ff8000">
          <convert type="g17EventTime">StartTime</convert>
        </widget>
        <widget position="279,846" size="552,57" source="session.Event_Now" transparent="1" backgroundColor="#00000000" valign="center" render="g17EmptyEpg" readTagInfo="1" zPosition="7" font="Prive4;34"  noWrap="1" foregroundColor="#00ff8000">
          <convert type="EventName">Name</convert>
        </widget>
        <widget position="831,846" size="157,57" source="session.Event_Now" transparent="1" backgroundColor="#00000000" valign="center" render="Label" zPosition="6" font="Prive4;31"  foregroundColor="#00ff8000" halign="right">
          <convert type="g17EventTime">Remaining</convert>
        </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="209,902" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="209,902" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" /> 
       
        <widget position="153,925" size="120,45" source="session.Event_Next" transparent="1" backgroundColor="#00000000" valign="center" render="Label" font="Prive4;33"  zPosition="8" foregroundColor="#0000ff00">
          <convert type="g17EventTime">StartTime</convert>
        </widget>
        <widget position="279,925" size="567,45" source="session.Event_Next" transparent="1" backgroundColor="#00000000" valign="center" render="g17EmptyEpg" font="Prive4;34"  zPosition="7" noWrap="1" foregroundColor="#0000ff00">
          <convert type="EventName">Name</convert>
        </widget>
        <widget position="831,925" size="142,45" source="session.Event_Next" transparent="1" backgroundColor="#00000000" valign="center" render="Label" font="Prive4;31"  zPosition="6" foregroundColor="#0000ff00" halign="right">
          <convert type="g17EventTime">Duration</convert>
        </widget>
        <widget source="session.FrontendInfo" render="g17TunersLabel" font="Regular2;28" alphatest="off" position="1002,862" size="217,33" tuners="5" ActiveTunerColor="#0000d100" backgroundColor="#00000000" BackgroundActiveTunerColor="#00ecb100" zPosition="2"/>
    <widget position="1002,903" size="217,33" source="session.RecordState" render="FixedLabel" text="R" font="Regular;28" valign="center" halign="center" foregroundColor="#00ff0000" backgroundColor="#00000000" transparent="1" zPosition="1">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>      
        <ePixmap position="316,672" size="175,138" pixmap="hd_glass17/frame25-fs8.png" zPosition="1" alphatest="on" />
        <widget name="picProvSat" position="328,693" size="150,90" zPosition="2" alphatest="on" />
    <widget name="weaTxt" position="328,693" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />

        <widget name="subserv" position="1728,852" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="blend" />
        <widget name="wide" position="1728,852" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="blend" />
        <widget name="dolby" position="1728,852" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="blend" />
        <widget name="multi_audio" position="1728,852" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="blend" />
        <widget name="txt" position="1728,852" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="blend" />
        <widget name="hd_sd" position="1728,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="blend" />
        <widget name="hbb" position="1728,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="blend" />
        <widget name="subtit" position="1728,852" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="blend" />
        <widget name="tuner" position="1728,852" size="0,0" zPosition="1" alphatest="blend" />
        <widget name="HDD_state" position="1728,852" size="42,72" zPosition="1" alphatest="blend" />   
          <widget name="ecmlabels" font="Prive3;24" position="108,172" zPosition="2" size="150,337" backgroundColor="#00000000" foregroundColor="#0000ff00" />
          <widget name="ecmValues" font="Prive3;24" position="190,172" zPosition="3" size="303,337" backgroundColor="#00000000" foregroundColor="#00ffffff" />
        <widget name="picProv" position="120,61"  size="150,90"  zPosition="1" alphatest="on"/>
        <widget name="picSat" position="318,61"  size="150,90"  zPosition="1" alphatest="on"/>
        <widget name="piconEcm" position="120,519"  size="150,90"  zPosition="2" alphatest="on"/>
        <widget name="piconCam" position="318,519"  size="150,90"  zPosition="2" alphatest="on"/>
        <widget name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="#00000000" />
        <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="#00000000" />
        <eLabel position="126,844" size="1663,126" backgroundColor="#00000000" zPosition="-1" transparent="0" />
        <eLabel position="52,1011" size="1809,69" backgroundColor="#00000000" zPosition="-1" transparent="0" />"""
g17_extraScreen["33"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/33/infobar-29-2-fs8.png" alphatest="off" />\n'
g17_extraScreen["33"]  += '<widget name="back_enhanced" position="60,7"  size="465,660" pixmap="'+PATH+'/33/back_enhanced25-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["33"]  += '<widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="'+PATH+'/33/back_caidPidsX-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["33"]  += '<widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="'+PATH+'/33/end_caidPids26-fs8.png" alphatest="off" zPosition="3" />\n'  
g17_extraScreen["33"]  += """</screen>"""

g17_extraScreen["34"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""
g17_extraScreen["34"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/34/infobar-34b.png" alphatest="off" />\n'
g17_extraScreen["34"]  += """<widget name="Video_size" font="Prive4;27" position="70,778" size="210,33" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget source="session.CurrentService" render="Label" position="285,777" size="120,39" font="Prive4;33" halign="left" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2" valign="bottom">
      <convert type="g17ServiceNum">Number</convert>
    </widget>
    <widget position="381,771" size="757,48" source="session.CurrentService" render="Label" font="Prive4;39" valign="bottom" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="ServiceName">Name</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="979,778" size="660,33" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1651,771" size="135,48" font="Prive4;39" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1767,774" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <ePixmap position="81,834" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="100,850" size="150,90" zPosition="2" transparent="1" alphatest="on" />   
  
    <widget name="Prov_temp_rpm" position="1039,844" size="0,0" font="Prive4;24" valign="center" halign="center" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" />
    
    <widget position="285,847" size="90,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="381,847" size="645,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1029,847" size="142,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="358,892" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="358,892" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />    
    <widget position="285,919" size="90,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="381,919" size="645,39" source="session.Event_Next" render="g17EmptyEpg" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1029,919" size="142,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1795,841" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" backgroundColor="black" alphatest="blend" />
    <widget name="wide" position="1795,841" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" backgroundColor="black" alphatest="blend" />
    <widget name="dolby" position="1795,841" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" backgroundColor="black" alphatest="blend" />
    <widget name="multi_audio" position="1795,841" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" backgroundColor="black" alphatest="blend" />
    <widget name="txt" position="1795,841" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" backgroundColor="black" alphatest="blend" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="on" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="on" />
    <widget name="subtit" position="1795,841" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" backgroundColor="black" alphatest="blend" />
    <widget name="tuner" position="1795,841" size="42,72" zPosition="1" backgroundColor="black" alphatest="blend" />
    <widget name="HDD_state" position="1795,841" size="42,72" zPosition="1" backgroundColor="black" alphatest="blend" />    
    <widget position="1795,841" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" backgroundColor="black" alphatest="blend">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
    <widget name="TP_type" position="1544,979" zPosition="2" size="293,30" font="Prive4;22" halign="right" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" />
    <widget name="TP_info" position="894,978" zPosition="1" size="735,30" font="Prive4;24" halign="right" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" />

    <widget name="Dtype" position="1759,916" size="78,46" zPosition="3" backgroundColor="black" alphatest="blend" />
    <widget name="Dcam" position="1759,916" size="78,46" zPosition="3" backgroundColor="black" alphatest="blend" />
    <widget name="Decm" position="1759,916" size="78,46" zPosition="3" backgroundColor="black" alphatest="blend" />
    <widget name="Dnetstate" position="1759,916" size="78,46" zPosition="3" backgroundColor="black" alphatest="blend" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1759,916" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1759,916" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1759,916" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1759,916" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1759,916" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1759,916" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1759,916" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1759,916" size="78,46" zPosition="3" alphatest="blend" />
      	
    <eLabel text="Snr:" font="Prive4;24" position="87,978" size="105,30" foregroundColor="un99bad6" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" />
    <widget source="session.FrontendStatus" render="Label" position="147,978" size="90,30" font="Prive4;24" zPosition="5" foregroundColor="unb2e0b4" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="237,978" size="60,30" font="Prive4;24" foregroundColor="un99bad6" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" />
    <widget source="session.FrontendStatus" render="Label" position="297,978" size="90,30" font="Prive4;24" foregroundColor="unb2e0b4" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <widget name="bitrate_info" position="387,978" zPosition="8" size="750,30" font="Prive3;24" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1"/>

    <widget name="ecmLineInfo" position="780,994" size="0,0" font="Prive4;18" noWrap="1" halign="right" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" foregroundColor="unb2e0b4" zPosition="5" />

		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,573"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,573"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />"""
g17_extraScreen["34"]  += '<widget name="back_enhanced" position="60,60"  size="465,660" pixmap="'+PATH+'/34/back_enhancedX-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["34"]  += '<widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="'+PATH+'/34/back_caidPidsX-fs8.png" alphatest="off" zPosition="0" />\n'
g17_extraScreen["34"]  += """<widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />    
  </screen>"""

g17_extraScreen["35"] = """
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""
g17_extraScreen["35"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/35/infobar-35-fs8.png" alphatest="off" />\n'
g17_extraScreen["35"]  += """
    <widget position="283,772" size="757,52" source="session.CurrentService" render="Label" font="Prive4;39" zPosition="2" valign="top" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <ePixmap position="90,957" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="930,957" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="982,957" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <widget name="TP_info" position="288,966" zPosition="1" size="750,30" font="Prive3;24" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="TP_type" position="91,967" zPosition="2" size="293,30" font="Prive3;22" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="Video_size" font="Prive4;27" position="85,781" size="180,33" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1639,769" size="135,48" font="Prive4;39" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1755,772" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="967,781" size="660,30" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="1090,841" size="547,37" font="Prive4;27" halign="right" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1753,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1753,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1753,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1753,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1753,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1753,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1753,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1753,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1753,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1753,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1753,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1753,966" size="78,46" zPosition="3" alphatest="off" />
    
    <ePixmap position="81,834" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="100,850" size="150,90" zPosition="2" transparent="1" alphatest="on" />

    <widget position="285,873" size="90,39" source="session.Event_Now" render="Label" zPosition="1" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="381,873" size="555,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="939,873" size="142,39" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="313,837" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="313,837" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />
    <widget position="285,907" size="90,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="381,907" size="555,39" source="session.Event_Next" transparent="1" backgroundColor="background" render="g17EmptyEpg" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="939,907" size="142,39" source="session.Event_Next" transparent="1" backgroundColor="background" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    <widget name="subserv" position="1606,886" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1606,886" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1606,886" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1606,886" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1606,886" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1606,886" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1606,886" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1606,886" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1606,886" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>

    <widget name="bitrate_info" position="91,1003" zPosition="8" size="750,30" font="Prive3;24" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1"/>    
    <widget name="ecmLineInfo" position="780,1009" size="1047,24" font="Prive4;18" transparent="1" noWrap="1" halign="right" backgroundColor="background" foregroundColor="unb2e0b4" zPosition="5" />

    <widget source="session.FrontendStatus" render="Progress" position="1672,834" size="7,112" zPosition="4" pixmap="hd_glass17/icons/bar.png" orientation="orBottomToTop" transparent="1" >
    <convert type="g17ExtraSource">SnrNum</convert>                          
    </widget>
    <widget source="session.FrontendStatus" render="Progress" position="1815,834" size="7,112" zPosition="4" pixmap="hd_glass17/icons/bar.png" orientation="orBottomToTop" transparent="1" >
    <convert type="g17ExtraSource">AgcNum</convert>
    </widget>

    <ePixmap pixmap="hd_glass17/icons/bar_back_snr.png" position="1672,834" size="7,112" zPosition="1" alphatest="on"/>
    <ePixmap pixmap="hd_glass17/icons/bar_back.png" position="1815,834" size="7,112" zPosition="1" alphatest="on"/>

    <eLabel text="Snr:" font="Prive3;22" position="1692,834" zPosition="2" size="142,30" halign="left" backgroundColor="background" foregroundColor="green" transparent="1" />
    <eLabel text="Agc:" font="Prive3;22" position="1692,876" zPosition="2" size="142,30" halign="left" backgroundColor="background" foregroundColor="yellow" transparent="1" />
    <eLabel text="Ber:" font="Prive3;22" position="1692,918" zPosition="4" size="142,30" halign="left" backgroundColor="background" foregroundColor="red" transparent="1" />

    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="1744,834" zPosition="5" backgroundColor="background" foregroundColor="white" size="105,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="1744,876" zPosition="5" backgroundColor="background" foregroundColor="white" size="105,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" 	font="Prive3;22" position="1744,918" zPosition="5" backgroundColor="background" foregroundColor="white" size="105,30" halign="left" transparent="1"  >
    <convert type="g17ExtraSource">BerText</convert> 
    </widget>

		<widget name="ecmlabels" font="Prive3;24" position="108,210" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,210" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,45"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,99"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,99"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,556"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,556"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,90" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,90" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    
  </screen>"""
  
g17_extraScreen["36"] = """
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""
g17_extraScreen["36"]  += '<ePixmap position="0,649" zPosition="-2" size="1920,430" pixmap="'+PATH+'/36/infobar-fs8.png" alphatest="off" />\n'
g17_extraScreen["36"]  += '<ePixmap position="60,798" size="189,123" pixmap="'+PATH+'/36/frame36-fs8.png" zPosition="1" alphatest="on" />\n'
g17_extraScreen["36"]  += '<widget source="session.Event_Now" render="Progress" pixmap="'+PATH+'/36/slider36-fs8.png" position="382,766" size="744,18" zPosition="3" transparent="1">\n'
g17_extraScreen["36"]  += '<convert type="EventTime">Progress</convert>\n'
g17_extraScreen["36"]  += '</widget>\n'
g17_extraScreen["36"]  += '<widget source="session.FrontendStatus" render="Progress" position="109,994" size="121,45" zPosition="4" pixmap="'+PATH+'/36/sig-bar36.png" transparent="1" >\n'
g17_extraScreen["36"]  += '<convert type="g17ExtraSource">SnrNum</convert>\n'                          
g17_extraScreen["36"]  += '</widget>\n'
g17_extraScreen["36"]  += '<widget source="session.FrontendStatus" render="Progress" position="387,994" size="121,45" zPosition="4" pixmap="'+PATH+'/36/sig-bar36.png" transparent="1" >\n'
g17_extraScreen["36"]  += '<convert type="g17ExtraSource">AgcNum</convert>\n'
g17_extraScreen["36"]  += '</widget>\n'
g17_extraScreen["36"]  += """
    <widget source="session.CurrentService" render="Label" position="108,694" size="96,39" font="Prive3;30" halign="center" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" zPosition="2" valign="top">
      <convert type="g17ServiceNum">Number</convert>
    </widget>
    <widget position="382,694" size="744,39" source="session.CurrentService" render="Label" font="Prive3;30" valign="top" halign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="ServiceName">Name</convert>
    </widget>
    <widget name="TP_info" position="277,946" zPosition="1" size="636,30" font="Prive3;22" halign="center" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="TP_type" position="73,946" zPosition="1" size="169,30" font="Prive3;20" halign="center" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="Video_size" font="Prive3;27" position="70,756" size="166,39" halign="center" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1657,694" size="183,33" font="Prive3;30" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="g17ClockToText">Format:%H:%M:%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A, %d.%B %Y" position="1003,697" size="660,33" font="Prive3;27" halign="right" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="1321,757" size="519,33" font="Prive3;27" halign="right" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" />
    <widget name="bitrate_info" position="1321,808" zPosition="8" size="519,33" font="Prive3;27" halign="right" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1"/>    

    <widget name="Dtype" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    
    <widget name="g17picon" position="79,814" size="150,90" zPosition="2" transparent="1" alphatest="on" />

    <widget position="285,810" size="100,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive3;28" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="391,810" size="697,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive3;28" valign="bottom" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1087,810" size="142,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive3;28" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget name="slider_back" position="382,765" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />
    <widget position="285,873" size="100,39" source="session.Event_Next" render="Label" font="Prive3;28" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="391,873" size="697,39" source="session.Event_Next" render="g17EmptyEpg" font="Prive3;28" valign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1087,873" size="142,39" source="session.Event_Next" render="Label" font="Prive3;28" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    <widget name="subserv" position="1818,853" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1818,853" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1818,853" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1818,853" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1818,853" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1818,853" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1818,853" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1818,853" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1818,853" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>

    <widget name="ecmLineInfo" position="583,997" size="1273,30" font="Prive3;22" noWrap="1" halign="right" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" zPosition="5" />

    <eLabel text="Q:" font="Prive3;22" position="85,1000" zPosition="2" size="90,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <eLabel text="S:" font="Prive3;22" position="361,1000" zPosition="2" size="90,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="237,1000" zPosition="5" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" size="90,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="513,1000" zPosition="5" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" size="90,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">AgcText</convert>
    </widget>

		<widget name="ecmlabels" font="Prive3;24" position="108,187" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,187" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" alphatest="off" position="60,22"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" zPosition="0" />
    <widget name="picProv" position="120,76"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,76"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,534"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,534"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="caidPids" transparent="1" position="1639,82" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,22"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,82" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,93"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    
  </screen>""" 
  
g17_extraScreen["37"] = """
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""
g17_extraScreen["37"]  += '<ePixmap position="0,649" zPosition="-2" size="1920,430" pixmap="'+PATH+'/37/infobar37-fs8.png" alphatest="off" />\n'
g17_extraScreen["37"]  += '<ePixmap position="60,798" size="189,123" pixmap="'+PATH+'/37/frame36-fs8.png" zPosition="1" alphatest="on" />\n'
g17_extraScreen["37"]  += '<widget source="session.Event_Now" render="Progress" pixmap="'+PATH+'/37/slider36-fs8.png" position="382,766" size="744,18" zPosition="3" transparent="1">\n'
g17_extraScreen["37"]  += '<convert type="EventTime">Progress</convert>\n'
g17_extraScreen["37"]  += '</widget>\n'
g17_extraScreen["37"]  += '<widget source="session.FrontendStatus" render="Progress" position="109,994" size="121,45" zPosition="4" pixmap="'+PATH+'/37/sig-bar36.png" transparent="1" >\n'
g17_extraScreen["37"]  += '<convert type="g17ExtraSource">SnrNum</convert>\n'                          
g17_extraScreen["37"]  += '</widget>\n'
g17_extraScreen["37"]  += '<widget source="session.FrontendStatus" render="Progress" position="387,994" size="121,45" zPosition="4" pixmap="'+PATH+'/37/sig-bar36.png" transparent="1" >\n'
g17_extraScreen["37"]  += '<convert type="g17ExtraSource">AgcNum</convert>\n'
g17_extraScreen["37"]  += '</widget>\n'
g17_extraScreen["37"]  += """
    <widget source="session.CurrentService" render="Label" position="108,694" size="96,39" font="Prive3;30" halign="center" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" zPosition="2" valign="top">
      <convert type="g17ServiceNum">Number</convert>
    </widget>
    <widget position="382,694" size="744,39" source="session.CurrentService" render="Label" font="Prive3;30" valign="top" halign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="ServiceName">Name</convert>
    </widget>
    <widget name="TP_info" position="277,946" zPosition="1" size="636,30" font="Prive3;22" halign="center" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="TP_type" position="73,946" zPosition="1" size="169,30" font="Prive3;20" halign="center" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="Video_size" font="Prive3;27" position="70,756" size="166,39" halign="center" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1657,694" size="183,33" font="Prive3;30" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="g17ClockToText">Format:%H:%M:%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A, %d.%B %Y" position="1003,697" size="660,33" font="Prive3;27" halign="right" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="1321,757" size="519,33" font="Prive3;27" halign="right" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" />
    <widget name="bitrate_info" position="1321,808" zPosition="8" size="519,33" font="Prive3;27" halign="right" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1"/>    

    <widget name="Dtype" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1782,939" size="78,46" zPosition="3" alphatest="off" />
    
    <widget name="g17picon" position="79,814" size="150,90" zPosition="2" transparent="1" alphatest="on" />

    <widget position="285,810" size="100,39" source="session.Event_Now" render="Label" backgroundColor="background" transparent="1" zPosition="1" font="Prive3;28" valign="center" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="391,810" size="697,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" backgroundColor="background" transparent="1" zPosition="-1" font="Prive3;28" valign="bottom" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1087,810" size="142,39" source="session.Event_Now" render="Label" zPosition="1" backgroundColor="background" transparent="1" font="Prive3;28" valign="center" foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget name="slider_back" position="382,765" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />
    <widget position="285,873" size="100,39" source="session.Event_Next" render="Label" font="Prive3;28" backgroundColor="background" transparent="1" valign="center" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="391,873" size="697,39" source="session.Event_Next" render="g17EmptyEpg" backgroundColor="background" transparent="1" font="Prive3;28" valign="center" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1087,873" size="142,39" source="session.Event_Next" render="Label" font="Prive3;28" backgroundColor="background" transparent="1" valign="center" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    <widget name="subserv" position="1818,853" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1818,853" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1818,853" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1818,853" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1818,853" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1818,853" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1818,853" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1818,853" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1818,853" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>

    <widget name="ecmLineInfo" position="583,997" size="1273,30" font="Prive3;22" noWrap="1" halign="right" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" zPosition="5" />

    <eLabel text="Q:" font="Prive3;22" position="85,1000" zPosition="2" size="90,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <eLabel text="S:" font="Prive3;22" position="361,1000" zPosition="2" size="90,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="237,1000" zPosition="5" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" size="90,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="513,1000" zPosition="5" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" size="90,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">AgcText</convert>
    </widget>

		<widget name="ecmlabels" font="Prive3;24" position="108,187" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,187" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,22"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,76"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,76"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,534"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,534"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,82" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,22"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,82" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,93"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    
  </screen>"""   
  
g17_extraScreen["38"] = """
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""
g17_extraScreen["38"]  += '<ePixmap position="0,649" zPosition="-2" size="1920,430" pixmap="'+PATH+'/38/infobar-ax-fs8.png" alphatest="off" />\n'
g17_extraScreen["38"]  += """
    <widget position="306,712" size="900,60" source="session.CurrentService" render="Label" font="Prive3;37" valign="center" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <widget name="TP_info" position="576,945" zPosition="1" size="765,40" font="Prive3;27" halign="center" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget name="TP_type" position="334,945" zPosition="1" size="213,40" font="Prive3;26" halign="center" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget name="Video_size" font="Prive3;27" position="99,724" size="189,37" halign="center" valign="enter" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1699,724" size="199,49" font="Prive3;30" valign="top" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="g17ClockToText">Format:%H:%M:%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A, %d.%B %Y" position="1024,729" size="660,49" font="Prive3;27" halign="right" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="1321,757" size="0,0" font="Prive3;27" halign="right" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" />
    <widget name="bitrate_info" position="1386,945" zPosition="8" size="427,36" font="Prive3;27" halign="center" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1"/>    

    <widget name="Dtype" position="1744,873" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1744,873" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1744,873" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1744,873" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1744,873" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1744,873" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1744,873" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1744,873" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1744,873" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1744,873" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1744,873" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1744,873" size="78,46" zPosition="3" alphatest="off" />
    
    <ePixmap position="99,792" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="118,808" size="150,90" zPosition="2" transparent="1" alphatest="on" />
    <widget position="298,792" size="100,39" source="session.Event_Now" render="Label" backgroundColor="background" transparent="1" zPosition="1" font="Prive3;28" valign="top" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="397,792" size="577,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" backgroundColor="background" transparent="1" zPosition="-1" font="Prive3;28" valign="top" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="973,792" size="142,39" source="session.Event_Now" render="Label" backgroundColor="background" transparent="1" zPosition="1" font="Prive3;28" valign="top" foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget name="slider_back" position="333,843" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="333,843" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget position="298,876" size="100,39" source="session.Event_Next" render="Label" backgroundColor="background" transparent="1" font="Prive3;28" valign="bottom" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="397,876" size="577,39" source="session.Event_Next" render="g17EmptyEpg" backgroundColor="background" transparent="1" font="Prive3;28" valign="bottom" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="973,876" size="142,39" source="session.Event_Next" render="Label" backgroundColor="background" transparent="1" font="Prive3;28" valign="bottom" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    <widget name="subserv" position="1782,793" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1782,793" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1782,793" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1782,793" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1782,793" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1782,793" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1782,793" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1782,793" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1782,793" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>

    <widget name="ecmLineInfo" position="105,1000" size="1722,27" font="Prive3;24" noWrap="1" halign="center" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" zPosition="5" />

    <widget source="session.FrontendStatus" render="Label" font="Prive3;27" position="97,945" size="193,40" halign="center" valign="center" zPosition="5" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" >
    <convert type="g17ExtraSource">SnrAgcTxt</convert>
    </widget>

		<widget name="ecmlabels" font="Prive3;24" position="108,187" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,187" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,22"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,76"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,76"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,534"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,534"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,82" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,22"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,82" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,93"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    
  </screen>""" 

g17_extraScreen["39"] = """
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""
g17_extraScreen["39"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/39/infobar-35-fs8.png" alphatest="off" />\n'
g17_extraScreen["39"]  += '<widget source="session.FrontendStatus" render="g17Progress" position="160,1029" size="800,6" zPosition="4" pixmap="'+PATH+'/39/level.png" transparent="1" >\n'
g17_extraScreen["39"]  += '<convert type="g17ExtraSource">SnrNum</convert>\n'
g17_extraScreen["39"]  += '</widget>\n'
g17_extraScreen["39"]  += '<widget source="session.FrontendStatus" render="g17Progress" position="1080,1029" size="800,6" zPosition="4" pixmap="'+PATH+'/39/level.png" transparent="1" >\n'
g17_extraScreen["39"]  += '<convert type="g17ExtraSource">AgcNum</convert>\n'
g17_extraScreen["39"]  += '</widget>\n'
g17_extraScreen["39"]  += """
    <widget position="245,742" size="757,52" source="session.CurrentService" render="Label" font="Prive4;39" zPosition="2" valign="top" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <ePixmap position="50,927" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="890,927" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="1022,927" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <widget name="TP_info" position="248,936" zPosition="1" size="750,30" font="Prive3;24" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="TP_type" position="50,936" zPosition="2" size="293,30" font="Prive3;22" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="Video_size" font="Prive4;27" position="45,751" size="180,33" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1679,739" size="135,48" font="Prive4;39" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1795,742" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="1007,751" size="660,33" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="1116,806" size="547,37" font="Prive4;27" halign="right" backgroundColor="background" transparent="1" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1431,966" size="78,46" zPosition="1" alphatest="off" />
    <widget name="Dcam" position="1431,966" size="78,46" zPosition="1" alphatest="off" />
    <widget name="Decm" position="1431,966" size="78,46" zPosition="1" alphatest="off" />
    <widget name="Dnetstate" position="1431,966" size="78,46" zPosition="1" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1431,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1431,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1431,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1431,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1431,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1784,936" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1431,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1431,966" size="78,46" zPosition="3" alphatest="off" />
    
    <ePixmap position="41,804" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="60,820" size="150,90" zPosition="2" transparent="1" alphatest="on" />

    <widget position="245,836" size="90,39" source="session.Event_Now" backgroundColor="background" transparent="1" render="Label" zPosition="1" font="Prive4;29" valign="bottom" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="341,836" size="635,39" source="session.Event_Now" backgroundColor="background" transparent="1" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive4;29" valign="bottom" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="979,836" size="142,39" source="session.Event_Now" backgroundColor="background" transparent="1" render="Label" zPosition="1" font="Prive4;29" valign="bottom" foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="313,807" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="313,807" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />
    <widget position="245,881" size="90,39" source="session.Event_Next" backgroundColor="background" transparent="1" render="Label" font="Prive4;29" valign="bottom" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="341,881" size="635,39" source="session.Event_Next" backgroundColor="background" transparent="1" render="g17EmptyEpg" font="Prive4;29" valign="bottom" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="979,881" size="142,39" source="session.Event_Next" backgroundColor="background" transparent="1" render="Label" font="Prive4;29" valign="bottom" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    <widget name="subserv" position="1632,856" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1632,856" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1632,856" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1632,856" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1632,856" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1632,856" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1632,856" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1632,856" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1632,856" size="0,0" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1632,856" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1632,856" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1632,886" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
    <widget name="bitrate_info" position="560,986" zPosition="8" size="365,24" noWrap="1" font="Prive4;18" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1"/>    
    <widget name="ecmLineInfo" position="823,986" size="1038,24" font="Prive4;18" noWrap="1" halign="right" backgroundColor="background" transparent="1" foregroundColor="unb2e0b4" zPosition="5" />
    <widget source="session.FrontendInfo" render="g17TunersLabel" alphatest="off" PosLR="L" font="Regular2;30" position="50,976" size="600,30" tuners="10" ActiveTunerColor="#0000d100" backgroundColor="background" BackgroundActiveTunerColor="#00ecb100" zPosition="2"/>  

    <ePixmap position="1680,804" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1699,820" size="150,90" zPosition="2" transparent="1" alphatest="on" />
    <widget name="weaTxt" position="1699,820" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />

    <eLabel text="Q:" font="Prive3;22" position="50,1020" zPosition="2" size="30,25" halign="left" backgroundColor="background" foregroundColor="white" transparent="1" />
    <eLabel text="S:" font="Prive3;22" position="970,1020" zPosition="2" size="30,25" halign="left" backgroundColor="background" foregroundColor="white" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="80,1020" zPosition="5" backgroundColor="background" foregroundColor="white" size="105,25" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="1000,1020" zPosition="5" backgroundColor="background" foregroundColor="white" size="105,25" halign="left" transparent="1" >
    <convert type="g17ExtraSource">AgcText</convert>
    </widget>

		<widget name="ecmlabels" font="Prive3;24" position="108,210" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,210" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,45"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,99"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,99"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,556"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,556"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,90" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,90" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    
  </screen>"""
      
g17_extraScreen["40"] = """                                                                                

    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent" zPosition="1">"""
g17_extraScreen["40"]  += '<ePixmap position="60,732" zPosition="-1" size="1800,345" pixmap="'+PATH+'/40/infoback.png" alphatest="on" />\n'
g17_extraScreen["40"]  += """<widget name="Video_size" font="Prive4;30" position="78,766" size="217,33" halign="center" backgroundColor="lightblue" transparent="1" />

    <widget source="session.CurrentService" render="Label" position="292,757" size="135,48" font="Prive4;39" halign="left" transparent="1" backgroundColor="black" foregroundColor="red" shadowColor="#551A8B" shadowOffset="-2,-1" zPosition="2" valign="bottom">
      <convert type="g17ServiceNum">Number</convert>
    </widget>
    <widget position="412,757" size="757,49" source="session.CurrentService" render="Label" font="Prive4;40" valign="bottom" halign="left" backgroundColor="black" foregroundColor="red" shadowColor="#551A8B" shadowOffset="-2,-1" zPosition="2" transparent="1">
      <convert type="ServiceName">Name</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="964,762" size="660,39" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1636,757" size="135,45" font="Prive4;36" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1752,760" size="75,39" font="Prive4;33" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <ePixmap position="81,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="100,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />   
  
    <widget name="Prov_temp_rpm" position="1045,820" size="589,37" font="Prive3;28" halign="right" backgroundColor="black" transparent="1" foregroundColor="orange" /> 
    
    <ePixmap position="1650,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1669,835" size="150,90" zPosition="2" transparent="1" alphatest="on" /> 
    <widget name="weaTxt" position="1669,835" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
    
    <widget position="277,814" size="120,42" source="session.Event_Now" render="Label" zPosition="1" backgroundColor="black" transparent="1" font="Prive4;36" valign="bottom" foregroundColor="yellow">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="405,814" size="573,45" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" backgroundColor="black" transparent="1" zPosition="1" font="Prive4;36" valign="bottom" noWrap="1" foregroundColor="white">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="946,814" size="150,45" source="session.Event_Now" render="Label" zPosition="1" backgroundColor="black" transparent="1" font="Prive4;36" valign="bottom" foregroundColor="yellow" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slidermain.png" position="276,868" size="837,21" zPosition="2" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="276,868" size="837,21" pixmap="hd_glass17/slider/sliderback-fs8.png" zPosition="1" alphatest="on" />    
    <widget position="277,894" size="150,45" source="session.Event_Next" render="Label" font="Prive4;36" transparent="1" backgroundColor="black" valign="bottom" foregroundColor="white">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="405,894" size="580,45" source="session.Event_Next" render="g17EmptyEpg" transparent="1" backgroundColor="black" font="Prive4;36" valign="bottom" noWrap="1" foregroundColor="yellow">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="946,894" size="150,45" source="session.Event_Next" render="Label" transparent="1" backgroundColor="black" font="Prive4;36" valign="bottom" foregroundColor="white" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1606,871" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="3" alphatest="on" />
    <widget name="wide" position="1606,871" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="3" alphatest="on" />
    <widget name="dolby" position="1606,871" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="3" alphatest="on" />
    <widget name="multi_audio" position="1606,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="3" alphatest="on" />
    <widget name="txt" position="1606,871" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="3" alphatest="on" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="on" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="on" />
    <widget name="subtit" position="1606,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="3" alphatest="on" />
    <widget name="tuner" position="1606,871" size="42,72" zPosition="3" alphatest="on" />
    <widget name="HDD_state" position="1606,871" size="42,72" zPosition="1" alphatest="on" />    
    <widget position="1606,871" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="4" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
        
    <ePixmap position="97,945" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="300,945" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="987,945" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    
    <widget name="TP_info" position="525,954" zPosition="1" size="735,30" font="Regular;27" halign="left" backgroundColor="black" foregroundColor="white" />
    <widget name="TP_type" position="106,954" zPosition="1" size="308,30" font="Regular;27" halign="left" backgroundColor="black" foregroundColor="yellow" />
    
    <widget name="Dtype" position="1755,951" size="78,46" zPosition="3" backgroundColor="black" alphatest="blend" />
    <widget name="Dcam" position="1755,951" size="78,46" zPosition="3" backgroundColor="black" alphatest="blend" />
    <widget name="Decm" position="1755,951" size="78,46" zPosition="3" backgroundColor="black" alphatest="blend" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" backgroundColor="black" alphatest="on" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1755,951" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1755,951" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1755,951" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1755,951" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1755,951" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1755,951" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1755,951" size="78,46" zPosition="3" alphatest="blend" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1755,951" size="78,46" zPosition="3" alphatest="blend" />
       
   <widget source="session.FrontendStatus" render="Progress" position="195,1005" size="300,7" zPosition="2" pixmap="hd_glass17/slider/sigbar.png" transparent="1" >
    <convert type="g17ExtraSource">SnrNum</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Progress" position="675,1005" size="300,7" zPosition="2" pixmap="hd_glass17/slider/sigbar.png" transparent="1" >
    <convert type="g17ExtraSource">AgcNum</convert>
    </widget>

    <ePixmap pixmap="hd_glass17/slider/sigsnrbar_back.png" position="195,1005" size="300,7" zPosition="1" alphatest="off"/>
    <ePixmap pixmap="hd_glass17/slider/sigbar_back.png" position="675,1005" size="300,7" zPosition="1" alphatest="off"/>

    <eLabel text="Ber:" font="Prive3;27" position="1095,990" zPosition="4" size="142,30" halign="left" backgroundColor="background" foregroundColor="red" transparent="1" />

    <widget source="session.FrontendStatus" render="Label" 	font="Prive3;27" position="1155,990" zPosition="5" backgroundColor="background" foregroundColor="white" size="105,30" halign="left" transparent="1"  >
    <convert type="g17ExtraSource">BerText</convert> 
    </widget>
  
    <eLabel text="Snr:" font="Prive4;27" position="126,988" size="60,30" foregroundColor="green" backgroundColor="lightblue" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="510,988" size="75,33" font="Prive4;27" zPosition="1" backgroundColor="black" foregroundColor="white">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="607,988" size="60,30" font="Prive4;27" foregroundColor="yellow" backgroundColor="black" transparent="1"/>
    <widget source="session.FrontendStatus" render="Label" position="990,988" size="75,30" font="Prive4;27" backgroundColor="black" foregroundColor="white">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    
    <widget name="bitrate_info" position="1377,994" zPosition="8" size="750,30" font="Prive3;25" halign="left" backgroundColor="background" foregroundColor="red" transparent="1"/>
		<widget name="ecmlabels" font="Prive3;24" position="100,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="183,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="52,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="112,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="310,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="112,574"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="310,574"  size="150,90"  zPosition="2" alphatest="on"/> 
    <widget  name="caidPids" transparent="1" position="529,157" zPosition="1" size="195,600" font="Regular;22" halign="center" foregroundColor="yellow" backgroundColor="background" />
    <widget name="active_caidPid" transparent="1" position="529,157" zPosition="2" size="195,25" font="Regular;22" halign="center" foregroundColor="red" backgroundColor="background" />
    <widget name="caidPids_back" position="499,97"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />  	 	
    <widget name="caidPids_end" position="499,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />

	</screen>""" 

g17_extraScreen["41"] = """

  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <ePixmap position="567,687" size="780,138" pixmap="hd_glass17/frame-chname26-fs8.png" zPosition="1" alphatest="on" />    
     <widget position="579,718" size="750,75" source="session.CurrentService" render="Label" zPosition="2" font="Prive4;45" valign="center" halign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>

    <widget name="ecmLineInfo" position="775,1002" size="0,0" font="Prive4;18" noWrap="1" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" zPosition="5" transparent="1" />

    <widget name="TP_info" position="102,1002" zPosition="6" size="0,0" font="Prive4;21" noWrap="1" halign="left" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget name="TP_type" position="162,1002" zPosition="6" size="0,0" font="Prive4;24" halign="left" foregroundColor="un99bad6" />
    <widget name="Video_size" font="Prive4;27" position="115,766" size="0,0" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
  
		<widget source="global.CurrentTime" render="g17Ahours" position="1674,712" size="108,108" zPosition="4" alphatest="on" foregroundColor="#f23d21">
			<convert type="g17ExtraSource">secHand</convert>
		</widget>
		<widget source="global.CurrentTime" render="g17Ahours" position="1683,721" size="90,90" zPosition="3" foregroundColor="white" alphatest="on">
			<convert type="g17ExtraSource">minHand</convert>
		</widget>
		<widget source="global.CurrentTime" render="g17Ahours" position="1693,732" size="69,69" zPosition="2" foregroundColor="white" alphatest="on">
			<convert type="g17ExtraSource">hourHand</convert>
		</widget>

    <widget name="Prov_temp_rpm" position="1075,826" size="0,0" font="Prive4;27" halign="right" backgroundColor="background" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1675,954" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1675,954" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1675,954" size="78,46" zPosition="3" alphatest="off" />
    
    <ePixmap position="118,702" size="175,138" pixmap="hd_glass17/frame25-fs8.png" zPosition="1" alphatest="on" />
    <widget name="g17picon" position="130,723" size="150,90" zPosition="2" transparent="1" alphatest="on" />
    
    <widget position="162,883" size="90,36" source="session.Event_Now" backgroundColor="background" transparent="1" render="Label" zPosition="8" font="Prive4;27" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="258,883" size="589,36" source="session.Event_Now" backgroundColor="background" transparent="1" render="g17EmptyEpg" readTagInfo="1" zPosition="7" font="Prive4;27"  noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="840,883" size="142,36" source="session.Event_Now" backgroundColor="background" transparent="1" render="Label" zPosition="6" font="Prive4;27"  foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slidermain.png" position="162,967" size="837,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="162,967" size="837,21" pixmap="hd_glass17/slider/sliderback-fs8.png" zPosition="2" alphatest="on" />
 
    <widget position="162,922" size="90,30" source="session.Event_Next" backgroundColor="background" transparent="1" render="Label" font="Prive4;27"  zPosition="8" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="258,922" size="589,30" source="session.Event_Next" backgroundColor="background" transparent="1" render="g17EmptyEpg" font="Prive4;27"  zPosition="7" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="840,922" size="142,30" source="session.Event_Next" backgroundColor="background" transparent="1" render="Label" font="Prive4;27"  zPosition="6" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    
    <widget name="subserv" position="1713,882" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1713,882" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1713,882" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1713,882" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1713,882" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1713,882" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1713,882" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1713,882" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1713,882" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
		<widget name="ecmlabels" font="Prive3;24" position="108,202" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,202" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="picProv" position="120,91"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,91"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,551"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,551"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />"""

g17_extraScreen["41"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/41/infobar-25-4-fs8.png" alphatest="off" />\n'
g17_extraScreen["41"]  += '<ePixmap position="126,874" size="27,126" pixmap="'+PATH+'/41/bi-l-flat-fs8.png" zPosition="1" alphatest="on"/>\n'
g17_extraScreen["41"]  += '<ePixmap position="1761,874" size="28,126" pixmap="'+PATH+'/41/bi-r-flat-fs8.png" zPosition="1" alphatest="on"/>\n'
g17_extraScreen["41"]  += '<widget  name="back_enhanced" alphatest="off" position="60,37"  size="465,660" pixmap="'+PATH+'/41/back_enhanced25-fs8.png" zPosition="0" />\n'
g17_extraScreen["41"]  += '<widget name="caidPids_back" alphatest="off" position="1609,45"  size="255,600" pixmap="'+PATH+'/41/back_caidPidsX-fs8.png" zPosition="0" />\n'
g17_extraScreen["41"]  += '<widget name="caidPids_end" alphatest="off" position="1609,115"  size="255,30" pixmap="'+PATH+'/41/end_caidPids26-fs8.png" zPosition="3" />\n'    
g17_extraScreen["41"]  += """</screen>"""	
  
g17_extraScreen["42"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="hd_glass17/general/infobar-ex.png" alphatest="off" />

  	<widget name="Video_size" font="Prive4;28" position="100,766" size="217,33" halign="center" backgroundColor="lightblue" transparent="1" />

    <widget position="315,757" size="757,48" source="session.CurrentService" render="Label" font="Prive4;37" valign="bottom" halign="left" noWrap="1" backgroundColor="black" foregroundColor="red" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="937,762" size="660,30" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1609,757" size="135,48" font="Prive4;36" valign="top" halign="right" backgroundColor="black" foregroundColor="red" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1725,760" size="69,34" font="Prive4;30" valign="top" halign="right" backgroundColor="black" foregroundColor="blue" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <ePixmap position="111,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="130,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />   
  
    <widget name="Prov_temp_rpm" position="1027,832" size="607,37" font="Prive4;27" halign="right" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />

    <ePixmap position="1635,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1654,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />    
    <widget name="weaTxt" position="1654,835" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
    
    <widget position="315,828" size="112,39" source="session.Event_Now" render="Label" zPosition="1" transparent="1" backgroundColor="background" font="Prive4;31" valign="bottom" foregroundColor="green">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="426,828" size="495,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="-1" font="Prive4;31" valign="bottom" noWrap="1" foregroundColor="yellow">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,828" size="150,39" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" zPosition="1" font="Prive4;31" valign="bottom" foregroundColor="green" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="313,874" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="313,874" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />    
    <widget position="315,892" size="112,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;31" valign="bottom" foregroundColor="yellow">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="426,892" size="495,39" source="session.Event_Next" render="g17EmptyEpg" transparent="1" backgroundColor="background" font="Prive4;31" valign="bottom" noWrap="1" foregroundColor="green">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,892" size="150,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;31" valign="bottom" foregroundColor="yellow" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1597,871" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1597,871" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1597,871" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1597,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1597,871" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1597,871" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1597,871" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1597,871" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
        
    <ePixmap position="120,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="960,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <widget name="TP_type" position="121,952" zPosition="2" size="293,30" font="Prive4;22" halign="left" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />
    <widget name="TP_info" position="315,951" zPosition="1" size="735,30" font="Prive4;24" halign="center" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1734,944" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1734,944" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1734,944" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,944" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1734,944" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1734,944" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1734,944" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1734,944" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1734,944" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1734,944" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1734,944" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1734,944" size="78,46" zPosition="3" alphatest="off" />
      	
  	<widget source="session.FrontendStatus" render="Progress" position="195,1005" size="300,7" zPosition="2" pixmap="hd_glass17/slider/sigbar.png" transparent="1" >
    <convert type="g17ExtraSource">SnrNum</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Progress" position="675,1005" size="300,7" zPosition="2" pixmap="hd_glass17/slider/sigbar.png" transparent="1" >
    <convert type="g17ExtraSource">AgcNum</convert>
    </widget>

    <ePixmap pixmap="hd_glass17/slider/sigsnrbar_back.png" position="195,1005" size="300,7" zPosition="1" alphatest="on"/>
    <ePixmap pixmap="hd_glass17/slider/sigbar_back.png" position="675,1005" size="300,7" zPosition="1" alphatest="on"/>

    <eLabel text="Ber:" font="Prive3;27" position="1095,990" zPosition="4" size="142,30" halign="left" backgroundColor="background" foregroundColor="red" transparent="1" />

    <widget source="session.FrontendStatus" render="Label" 	font="Prive3;27" position="1155,990" zPosition="5" backgroundColor="background" foregroundColor="white" size="105,30" halign="left" transparent="1"  >
    <convert type="g17ExtraSource">BerText</convert> 
    </widget>
  
    <eLabel text="Snr:" font="Prive4;27" position="126,988" size="60,30" foregroundColor="green" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="510,988" size="75,33" transparent="1" font="Prive4;27" zPosition="1" backgroundColor="background" foregroundColor="white">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="607,988" size="60,30" font="Prive4;27" foregroundColor="yellow" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="990,988" size="75,30" transparent="1" font="Prive4;27" backgroundColor="background" foregroundColor="white">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <widget name="ecmLineInfo" position="92,1024" size="1736,56" font="Prive4;20" noWrap="1" halign="center" valign="top" backgroundColor="background" transparent="1" zPosition="5" />
    <eLabel position="92,1024" size="1736,56" backgroundColor="background" zPosition="4" />
    
    <widget name="bitrate_info" position="1377,991" zPosition="8" size="750,30" font="Prive3;25" halign="left" backgroundColor="background" foregroundColor="red" transparent="1"/>
		<widget name="ecmlabels" font="Prive3;24" position="100,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="183,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="52,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="112,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="310,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="112,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="310,572"  size="150,90"  zPosition="2" alphatest="on"/> 
    <widget  name="caidPids" transparent="1" position="529,157" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="499,97"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="-1" />  	 	
    <widget name="active_caidPid" transparent="1" position="529,157" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="499,163"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />

	</screen>"""

g17_extraScreen["43"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="hd_glass17/general/infobar-ex.png" alphatest="off" />

  	<widget name="Video_size" font="Prive4;27" position="100,766" size="210,31" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />

    <widget source="session.CurrentService" render="Label" position="315,754" size="877,48" font="Prive4;39" halign="left" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2" valign="bottom">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="937,766" size="660,30" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1609,754" size="135,48" font="Prive4;39" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1725,757" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <ePixmap position="111,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="130,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />   
  
    <widget name="Prov_temp_rpm" position="1075,826" size="525,33" font="Prive3;27" halign="right" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

    <ePixmap position="1620,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1639,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />    
    <widget name="weaTxt" position="1639,835" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
    
    <widget position="315,828" size="90,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,828" size="495,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,828" size="142,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" halign="right" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="313,867" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="313,867" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />    
    <widget position="315,892" size="90,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,892" size="495,39" source="session.Event_Next" render="g17EmptyEpg" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6" transparent="1" backgroundColor="background">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,892" size="142,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" halign="right" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1569,871" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1569,871" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1569,871" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
    <ePixmap position="120,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="960,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <widget name="TP_type" position="121,952" zPosition="2" size="293,30" font="Prive4;22" halign="left" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget name="TP_info" position="315,951" zPosition="1" size="735,30" font="Prive4;24" halign="center" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />

    <widget name="Dtype" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
          	
  	<widget source="session.FrontendStatus" render="Progress" position="178,1002" size="230,6" zPosition="2" pixmap="hd_glass17/slider/sigbar43.png" transparent="1" >
    <convert type="g17ExtraSource">SnrNum</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Progress" position="554,1002" size="230,6" zPosition="2" pixmap="hd_glass17/slider/sigbar43.png" transparent="1" >
    <convert type="g17ExtraSource">AgcNum</convert>
    </widget>
    <ePixmap pixmap="hd_glass17/slider/sigsnrbar_back43.png" position="178,1002" size="230,6" zPosition="1" alphatest="on"/>
    <ePixmap pixmap="hd_glass17/slider/sigbar_back43.png" position="554,1002" size="230,6" zPosition="1" alphatest="on"/>
    <eLabel text="Snr:" font="Prive4;24" position="121,988" size="60,30" halign="left" foregroundColor="green" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="416,988" size="75,33" halign="left" transparent="1" font="Prive4;24" zPosition="1" backgroundColor="background" foregroundColor="white">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="496,988" size="60,30" font="Prive4;24" halign="left" foregroundColor="yellow" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="789,988" size="75,30" halign="left" transparent="1" font="Prive4;24" backgroundColor="background" foregroundColor="white">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>

    <widget name="ecmLineInfo" position="780,994" size="1017,24" font="Prive4;18" noWrap="1" halign="right" backgroundColor="background" foregroundColor="unb2e0b4" zPosition="5" transparent="1" />
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>	
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />

	</screen>"""

g17_extraScreen["44"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="hd_glass17/general/infobar-ex.png" alphatest="off" />

  	<widget name="Video_size" font="Prive4;27" position="100,766" size="210,31" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />

    <widget source="session.CurrentService" render="Label" position="315,754" size="877,48" font="Prive4;39" halign="left" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2" valign="bottom">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="937,766" size="660,30" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1609,754" size="135,48" font="Prive4;39" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1725,757" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <ePixmap position="111,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="130,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />   
  
    <widget name="Prov_temp_rpm" position="1075,826" size="525,33" font="Prive3;27" halign="right" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

    <ePixmap position="1620,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1639,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />    
    <widget name="weaTxt" position="1639,835" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
    
    <widget position="315,828" size="90,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,828" size="495,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,828" size="142,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" halign="right" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="313,867" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="313,867" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />    
    <widget position="315,892" size="90,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,892" size="495,39" source="session.Event_Next" render="g17EmptyEpg" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6" transparent="1" backgroundColor="background">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,892" size="142,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" halign="right" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1569,871" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1569,871" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1569,871" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
    <ePixmap position="120,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="960,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <widget name="TP_type" position="121,952" zPosition="2" size="293,30" font="Prive4;22" halign="left" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget name="TP_info" position="315,951" zPosition="1" size="735,30" font="Prive4;24" halign="center" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />

    <widget name="Dtype" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
          	
    <eLabel text="Snr: dB" font="Prive4;24" position="121,988" size="105,30" foregroundColor="un99bad6" transparent="1" backgroundColor="background"/>
    <widget source="session.FrontendStatus" render="Label" position="226,988" size="90,30" font="Prive4;24" zPosition="5" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17ExtraSource">SnrdB</convert>
    </widget>
    <ePixmap pixmap="hd_glass17/slider/sigsnrbar_back44.png" position="366,1002" size="230,6" zPosition="1" alphatest="on"/>
  	<widget source="session.FrontendStatus" render="Progress" position="366,1002" size="230,6" zPosition="2" pixmap="hd_glass17/slider/sigbar44.png" transparent="1" >
    <convert type="g17ExtraSource">SnrNum</convert>
    </widget>
    <eLabel text="Snr:" font="Prive4;24" position="309,988" size="60,30" halign="left" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="604,988" size="90,33" halign="left" transparent="1" font="Prive4;24" zPosition="1" backgroundColor="background" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Ber:" position="696,988" size="60,30" font="Prive4;24" halign="left" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="756,988" size="90,30" font="Prive4;24" foregroundColor="unefb2b2" transparent="1" backgroundColor="background">
      <convert type="g17ExtraSource">BerText</convert>
    </widget>

    <widget name="ecmLineInfo" position="780,994" size="1017,24" font="Prive4;18" noWrap="1" halign="right" backgroundColor="background" foregroundColor="unb2e0b4" zPosition="5" transparent="1" />
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>	
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />

	</screen>"""

g17_extraScreen["45"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="hd_glass17/general/infobar-ex.png" alphatest="off" />

  	<widget name="Video_size" font="Prive4;27" position="100,766" size="210,31" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />

    <widget source="session.CurrentService" render="Label" position="315,754" size="877,48" font="Prive4;39" halign="left" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2" valign="bottom">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="937,766" size="660,30" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1609,754" size="135,48" font="Prive4;39" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1725,757" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <ePixmap position="111,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="130,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />   
  
    <widget name="Prov_temp_rpm" position="1075,826" size="525,33" font="Prive3;27" halign="right" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

    <ePixmap position="1620,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1639,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />    
    <widget name="weaTxt" position="1639,835" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
    
    <widget position="315,828" size="90,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,828" size="495,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,828" size="142,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" halign="right" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="313,872" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="313,872" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />    
    <widget position="315,892" size="90,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,892" size="495,39" source="session.Event_Next" render="g17EmptyEpg" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6" transparent="1" backgroundColor="background">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,892" size="142,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" halign="right" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1569,871" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1569,871" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1569,871" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
    <ePixmap position="120,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="960,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <widget name="TP_type" position="121,952" zPosition="2" size="293,30" font="Prive4;22" halign="left" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget name="TP_info" position="315,951" zPosition="1" size="735,30" font="Prive4;24" halign="center" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />

    <widget name="Dtype" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
          	
    <eLabel text="Snr: dB" font="Prive4;20" position="121,988" size="105,30" halign="left" foregroundColor="un99bad6" transparent="1" backgroundColor="background"/>
    <widget source="session.FrontendStatus" render="Label" position="414,988" size="90,30" font="Prive4;20" halign="right" zPosition="5" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17ExtraSource">SnrdB</convert>
    </widget>
    <ePixmap pixmap="hd_glass17/slider/sigsnrbar_back44.png" position="206,998" size="230,6" zPosition="1" alphatest="on"/>
  	<widget source="session.FrontendStatus" render="Progress" position="206,998" size="230,6" zPosition="2" pixmap="hd_glass17/slider/sigbar44.png" transparent="1" >
    <convert type="g17ExtraSource">SnrNum</convert>
    </widget>
    <widget name="bitrate_info" position="516,988" zPosition="4" size="400,30" font="Prive4;20" halign="left" backgroundColor="background" transparent="1"/>    
    <widget name="ecmLineInfo" position="780,994" size="1017,24" font="Prive4;18" noWrap="1" halign="right" backgroundColor="background" foregroundColor="unb2e0b4" zPosition="5" transparent="1" />
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>	
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    </screen>"""
	
g17_extraScreen["46"] = """
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""
g17_extraScreen["46"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/46/infobar-46-fs8.png" alphatest="off" />\n'
g17_extraScreen["46"]  += '<widget source="session.FrontendStatus" render="Progress" position="1668,739" size="121,45" zPosition="4" pixmap="'+PATH+'/46/sig-bar36.png" transparent="1" >\n'
g17_extraScreen["46"]  += '<convert type="g17ExtraSource">SnrNum</convert>\n'                          
g17_extraScreen["46"]  += '</widget>\n'
g17_extraScreen["46"]  += '<widget source="session.FrontendStatus" render="Progress" position="1668,784" size="121,45" zPosition="4" pixmap="'+PATH+'/46/sig-bar36.png" transparent="1" >\n'
g17_extraScreen["46"]  += '<convert type="g17ExtraSource">AgcNum</convert>\n'
g17_extraScreen["46"]  += '</widget>\n'
g17_extraScreen["46"]  += """<widget position="675,684" size="637,39" source="session.CurrentService" render="Label" font="Prive3;30" zPosition="2" valign="top" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    
    <widget name="TP_info" position="277,1011" zPosition="1" size="636,30" font="Prive3;22" halign="center" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="TP_type" position="63,1011" zPosition="1" size="179,30" font="Prive3;22" halign="center" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="Video_size" font="Prive3;27" position="60,684" size="600,39" halign="center" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1672,684" size="183,33" font="Prive3;30" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="g17ClockToText">Format:%H:%M:%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A, %d.%B %Y" position="1041,685" size="660,33" font="Prive3;27" halign="right" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="681,892" size="540,33" font="Prive3;27" halign="center" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" />
    <widget name="bitrate_info" position="681,943" zPosition="8" size="540,33" font="Prive3;27" halign="center" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1"/>    

    <widget name="Dtype" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    
    <widget name="g17picon" position="60,738" size="600,255" zPosition="2" transparent="1" alphatest="on" />

    <widget position="675,783" size="105,45" source="session.Event_Now" render="Label" zPosition="1" font="Prive3;34" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="780,783" size="783,45" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive3;36" valign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1">
      <convert type="EventName">Name</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="780,753" size="762,21" zPosition="6" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="780,753" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="5" alphatest="on" />

    <widget position="675,835" size="105,45" source="session.Event_Next" render="Label" font="Prive3;34" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="780,835" size="783,45" source="session.Event_Next" render="g17EmptyEpg" font="Prive3;36" valign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1">
      <convert type="EventName">Name</convert>
    </widget>

    <widget name="subserv" position="1818,919" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1818,919" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1818,919" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1818,919" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1818,919" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1818,919" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1818,919" size="0,0" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1818,919" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1578,838" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>

    <widget name="ecmLineInfo" position="583,997" size="0,0" font="Prive3;22" noWrap="1" halign="right" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" zPosition="5" />

    <eLabel text="Q:" font="Prive3;22" position="1644,750" zPosition="2" size="90,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <eLabel text="S:" font="Prive3;22" position="1644,795" zPosition="2" size="90,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="1795,750" zPosition="5" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" size="90,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="1795,795" zPosition="5" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" size="90,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">AgcText</convert>
    </widget>

    <widget source="session.FrontendInfo" render="g17TunersLabel" font="Regular2;33" alphatest="off" position="1638,838" size="210,75" tuners="12" ActiveTunerColor="#0000d100" backgroundColor="background" BackgroundActiveTunerColor="#00ecb100" zPosition="2"/>  

		<widget name="ecmlabels" font="Prive3;24" position="100,175" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="183,175" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="52,10" size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="112,64" size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="310,64" size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="112,522" size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="310,522" size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,82" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,22"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,82" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,93"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />  
  </screen>""" 

g17_extraScreen["47"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="hd_glass17/general/infobar-ex.png" alphatest="off" />

  	<widget name="Video_size" font="Prive4;28" position="100,766" size="217,33" halign="center" backgroundColor="lightblue" transparent="1" />

    <widget position="315,757" size="757,48" source="session.CurrentService" render="Label" font="Prive4;37" valign="bottom" halign="left" noWrap="1" backgroundColor="black" foregroundColor="red" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="937,762" size="660,30" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1609,757" size="135,48" font="Prive4;36" valign="top" halign="right" backgroundColor="black" foregroundColor="red" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1725,760" size="69,34" font="Prive4;30" valign="top" halign="right" backgroundColor="black" foregroundColor="blue" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <ePixmap position="111,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="130,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />   
  
    <widget name="Prov_temp_rpm" position="1027,832" size="607,37" font="Prive4;27" halign="right" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />

    <ePixmap position="1635,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1654,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />    
    <widget name="weaTxt" position="1654,835" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
    
    <widget position="315,828" size="112,39" source="session.Event_Now" render="Label" zPosition="1" transparent="1" backgroundColor="background" font="Prive4;31" valign="bottom" foregroundColor="green">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="426,828" size="495,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="-1" font="Prive4;31" valign="bottom" noWrap="1" foregroundColor="yellow">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,828" size="150,39" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" zPosition="1" font="Prive4;31" valign="bottom" foregroundColor="green" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="313,874" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="313,874" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />    
    <widget position="315,892" size="112,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;31" valign="bottom" foregroundColor="yellow">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="426,892" size="495,39" source="session.Event_Next" render="g17EmptyEpg" transparent="1" backgroundColor="background" font="Prive4;31" valign="bottom" noWrap="1" foregroundColor="green">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,892" size="150,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;31" valign="bottom" foregroundColor="yellow" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1597,871" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1597,871" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1597,871" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1597,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1597,871" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1597,871" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1597,871" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1597,871" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
        
    <ePixmap position="120,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="960,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <widget name="TP_type" position="121,952" zPosition="2" size="293,30" font="Prive4;22" halign="left" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />
    <widget name="TP_info" position="315,951" zPosition="1" size="735,30" font="Prive4;24" halign="center" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1734,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1734,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1734,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1734,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1734,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1734,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1734,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1734,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1734,944" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1734,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1734,951" size="78,46" zPosition="3" alphatest="off" />
      	
  	<widget source="session.FrontendStatus" render="Progress" position="345,1005" size="300,7" zPosition="2" pixmap="hd_glass17/slider/sigbar.png" transparent="1" >
    <convert type="g17ExtraSource">SnrNum</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Progress" position="825,1005" size="300,7" zPosition="2" pixmap="hd_glass17/slider/sigbar.png" transparent="1" >
    <convert type="g17ExtraSource">AgcNum</convert>
    </widget>

    <ePixmap pixmap="hd_glass17/slider/sigsnrbar_back.png" position="345,1005" size="300,7" zPosition="1" alphatest="on"/>
    <ePixmap pixmap="hd_glass17/slider/sigbar_back.png" position="825,1005" size="300,7" zPosition="1" alphatest="on"/>

    <eLabel text="Snr: dB" font="Prive4;27" position="121,988" size="125,30" foregroundColor="green" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="241,988" size="100,30" font="Prive4;27" transparent="1" backgroundColor="background" zPosition="5" foregroundColor="white">
      <convert type="g17ExtraSource">SnrdB</convert>
    </widget>
  
    <widget source="session.FrontendStatus" render="Label" position="660,988" size="75,33" transparent="1" font="Prive4;27" zPosition="1" backgroundColor="background" foregroundColor="white">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="757,988" size="60,30" font="Prive4;27" foregroundColor="yellow" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="1140,988" size="75,30" transparent="1" font="Prive4;27" backgroundColor="background" foregroundColor="white">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    
    <widget name="bitrate_info" position="1377,991" zPosition="8" size="750,30" font="Prive3;27" halign="left" backgroundColor="background" foregroundColor="red" transparent="1"/>
		<widget name="ecmlabels" font="Prive3;24" position="100,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="183,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="52,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="112,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="310,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="112,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="310,572"  size="150,90"  zPosition="2" alphatest="on"/> 
    <widget  name="caidPids" transparent="1" position="529,157" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="499,97"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="-1" />  	 	
    <widget name="active_caidPid" transparent="1" position="529,157" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="499,163"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />

	</screen>"""

g17_extraScreen["48"] = """
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""
g17_extraScreen["48"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/48/infobar-35-fs8.png" alphatest="off" />\n'
g17_extraScreen["48"]  += '<widget  name="back_enhanced" alphatest="off" position="52,75" size="465,601" pixmap="'+PATH+'/48/back_enhanced-51.png" zPosition="0" />\n'
g17_extraScreen["48"]  += '<widget name="caidPids_back" alphatest="off" position="1609,15" size="255,600" pixmap="'+PATH+'/48/back_caidPids-44.png" zPosition="0" />\n'
g17_extraScreen["48"]  += '<widget name="caidPids_end" alphatest="off" position="1609,85" size="255,9" pixmap="'+PATH+'/48/end_caidPids-44.png" zPosition="3" />\n'
g17_extraScreen["48"]  += """

    <eLabel backgroundColor="white" position="0,810" size="1920,1" zPosition="5" />  
    <widget position="715,821" size="550,39" source="session.CurrentService" render="Label" font="Prive3;30" zPosition="2" valign="top" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
            <convert type="ServiceName">Name</convert>
    </widget>
    <widget source="session.CurrentService" render="Label" position="500,821" size="200,39" font="Prive3;30" halign="right" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2" valign="top">
      <convert type="g17ServiceNum">Number</convert>
    </widget>    
       
    <widget name="TP_info" position="500,770" zPosition="1" size="636,30" font="Prive3;25" halign="left" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="TP_type" position="250,770" zPosition="1" size="210,30" font="Prive3;25" halign="right" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="Video_size" font="Prive3;27" position="50,770" size="200,33" halign="center" valign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1672,768" size="183,33" font="Prive3;30" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="g17ClockToText">Format:%H:%M:%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A, %d.%B %Y" position="1041,769" size="660,33" font="Prive3;27" halign="right" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="1252,932" size="450,33" font="Prive3;27" halign="center" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" />
    <widget name="bitrate_info" position="1252,975" zPosition="8" size="450,33" font="Prive3;27" halign="center" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1"/>    

    <ePixmap position="1690,929" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1709,945" size="150,90" zPosition="2" transparent="1" alphatest="on" />
    <widget name="weaTxt" position="1709,945" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
        
    <ePixmap position="65,819" size="426,192" zPosition="1" pixmap="hd_glass17/frame/FrameZ.png" transparent="1" alphatest="on" />
        
    <widget name="g17picon" position="78,830" size="400,170" zPosition="2" transparent="1" alphatest="on" />

    <widget position="503,895" size="122,37" source="session.Event_Now" backgroundColor="background" transparent="1" valign="left" render="Label" zPosition="1" font="Prive4;27" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="595,895" size="555,37" source="session.Event_Now" backgroundColor="background" transparent="1" valign="center" render="g17EmptyEpg" readTagInfo="1" zPosition="2" font="Prive4;27" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1095,895" size="120,37" source="session.Event_Now" backgroundColor="background" transparent="1" valign="center" render="Label" zPosition="3" font="Prive4;27"  foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_390.png" position="545,868" size="585,12" zPosition="6" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <eLabel backgroundColor="white" position="545,874" size="585,1" zPosition="5" />     
       
    <widget position="503,950" size="277,37" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="Label" font="Prive4;27"  zPosition="5" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="595,950" size="555,37" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="g17EmptyEpg" font="Prive4;27" zPosition="6" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1095,950" size="120,37" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="Label" font="Prive4;27"  zPosition="7" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    <widget name="Dtype" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1723,951" size="0,0" zPosition="3" alphatest="off" /> 
    <widget name="subserv" position="1818,864" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1818,864" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1818,864" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1818,864" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1818,864" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,861" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,861" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1818,864" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1818,864" size="0,0" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1818,864" size="42,72" zPosition="1" alphatest="off" />    
    
    <widget position="1250,781" size="18,18" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/rec.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>

    <widget name="ecmLineInfo" position="570,1017" size="1300,25" font="Prive3;22" noWrap="1" halign="left" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" zPosition="5" />

      <eLabel text="Snr:" font="Regular;24" position="80,1015" size="65,25" backgroundColor="background" foregroundColor="darkgrey" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="140,1015" backgroundColor="background" size="70,25" font="Regular;24" zPosition="1" foregroundColor="white">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" font="Regular;24" position="250,1015" size="60,25" backgroundColor="background" foregroundColor="darkgrey" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="310,1015" backgroundColor="background" size="75,25" font="Regular;24" foregroundColor="white">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <eLabel text="Ber:" font="Regular;24" position="420,1015" size="65,25" backgroundColor="background" foregroundColor="darkgrey" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" font="Regular;24" position="480,1015" backgroundColor="background" zPosition="5" foregroundColor="white" size="70,20" halign="left" transparent="1"  >
    <convert type="g17ExtraSource">BerText</convert> 
    </widget>
        
    <widget source="session.FrontendInfo" render="g17TunersLabel" alphatest="off" font="Regular2;33" position="1315,815" size="550,36" tuners="12" ActiveTunerColor="#0000d100" backgroundColor="background" BackgroundActiveTunerColor="#00ecb100" zPosition="2"/>
		<widget name="ecmlabels" font="Prive3;24" position="100,210" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="183,210" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="picProv" position="112,99" size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="310,99" size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="112,559" size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="310,559" size="150,90"  zPosition="2" alphatest="on"/>

    <widget  name="caidPids" transparent="1" position="1639,75" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="active_caidPid" transparent="1" position="1639,75" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    
  </screen>"""

g17_extraScreen["49"] = """
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""
g17_extraScreen["49"]  += '<widget  name="back_enhanced" alphatest="off" position="52,40" size="465,660" pixmap="'+PATH+'/49/back_enhanced-44.png" zPosition="0" />\n'
g17_extraScreen["49"]  += '<widget name="caidPids_back" alphatest="off" position="1609,15" size="255,600" pixmap="'+PATH+'/49/back_caidPids-44.png" zPosition="0" />\n'
g17_extraScreen["49"]  += '<widget name="caidPids_end" alphatest="off" position="1609,85" size="255,9" pixmap="'+PATH+'/49/end_caidPids-44.png" zPosition="3" />\n'
g17_extraScreen["49"]  += '<widget source="session.FrontendStatus" render="Progress" position="1357,889" size="121,45" zPosition="4" pixmap="'+PATH+'/49/sig-bar36.png" transparent="1" >\n'
g17_extraScreen["49"]  += '<convert type="g17ExtraSource">SnrNum</convert>\n'                          
g17_extraScreen["49"]  += '</widget>\n'
g17_extraScreen["49"]  += '<widget source="session.FrontendStatus" render="Progress" position="1611,889" size="121,45" zPosition="4" pixmap="'+PATH+'/49/sig-bar36.png" transparent="1" >\n'
g17_extraScreen["49"]  += '<convert type="g17ExtraSource">AgcNum</convert>\n'
g17_extraScreen["49"]  += '</widget>\n'
g17_extraScreen["49"]  += """<eLabel backgroundColor="background" position="0,735" size="1920,315" zPosition="-1" />
  <widget position="60,667" size="1350,67" source="session.CurrentService" render="Label" font="Prive4;57" zPosition="2" valign="center" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>

    <eLabel text="Q:" font="Prive3;22" position="1330,900" zPosition="2" size="90,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <eLabel text="S:" font="Prive3;22" position="1587,900" zPosition="2" size="90,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="1485,900" zPosition="5" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" size="90,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="1738,900" zPosition="5" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" size="90,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">AgcText</convert>
    </widget>

    <eLabel backgroundColor="white" position="1261,946" size="658,1" zPosition="8" />
    <widget name="TP_info" position="660,738" zPosition="8" size="600,45" font="Prive4;27"  valign="center" halign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget name="TP_type" position="1335,672" zPosition="1" size="0,0" font="Prive4;42"  valign="center" halign="right" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget name="Video_size" font="Prive4;27" position="127,738" size="450,45"  valign="center" halign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1320,667" size="525,67" font="Prive4;57"  valign="center" halign="right" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format:%H:%M</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A, %d.%B %Y" position="1185,738" size="660,45" font="Prive3;27" valign="center" halign="right" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="1260,960" size="585,37" font="Prive4;27" valign="center" halign="center" backgroundColor="background" foregroundColor="un99bad6" />

    <widget name="Dtype" position="882,892" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="882,892" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Decm" position="882,892" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="882,892" size="0,0" zPosition="3" alphatest="off" />

    <eLabel backgroundColor="white" position="0,784" size="1920,1" zPosition="8" />
    <widget name="g17picon" position="660,787" size="600,255" zPosition="2" transparent="1" alphatest="on" />
    
    <widget position="60,801" size="277,45" source="session.Event_Now" valign="center" render="Label" zPosition="1" font="Prive4;28" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="60,852" size="585,45" source="session.Event_Now" valign="center" render="g17EmptyEpg" readTagInfo="1" zPosition="2" font="Prive4;28" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="375,801" size="277,45" source="session.Event_Now" valign="center" render="Label" zPosition="3" font="Prive4;28"  foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_390.png" position="60,916" size="585,21" zPosition="6" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="60,916" size="0,0" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="5" alphatest="on" />
    <eLabel backgroundColor="white" position="60,922" size="585,1" zPosition="5" /> 
    <widget position="60,952" size="277,45" source="session.Event_Next" valign="center" render="Label" font="Prive4;28"  zPosition="5" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="60,1003" size="585,45" source="session.Event_Next" valign="center" render="g17EmptyEpg" font="Prive4;28" zPosition="6" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="375,952" size="277,45" source="session.Event_Next" valign="center" render="Label" font="Prive4;28"  zPosition="7" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1803,808" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1803,808" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1803,808" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1803,808" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1803,808" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1803,808" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1803,808" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1803,808" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1803,808" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
    <widget name="ecmLineInfo" position="780,994" size="0,0" font="Prive4;18" noWrap="1" halign="right" backgroundColor="background" foregroundColor="unb2e0b4" zPosition="5" />
    <widget name="bitrate_info" position="1275,1005" zPosition="6" size="570,45" font="Prive4;27" noWrap="1" valign="center" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" />

		<widget name="ecmlabels" font="Prive3;24" position="100,205" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="183,205" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="picProv" position="112,94" size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="310,94" size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="112,551" size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="310,551" size="150,90"  zPosition="2" alphatest="on"/>

    <widget  name="caidPids" transparent="1" position="1639,75" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="active_caidPid" transparent="1" position="1639,75" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    
  </screen>"""

g17_extraScreen["50"] = """
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""
g17_extraScreen["50"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/50/infobar-50-fs8.png" alphatest="off" />\n'
g17_extraScreen["50"]  += '<widget source="session.FrontendStatus" render="Progress" position="1366,790" size="121,45" zPosition="4" pixmap="'+PATH+'/50/sig-bar36.png" transparent="1" >\n'
g17_extraScreen["50"]  += '<convert type="g17ExtraSource">SnrNum</convert>\n'                          
g17_extraScreen["50"]  += '</widget>\n'
g17_extraScreen["50"]  += '<widget source="session.FrontendStatus" render="Progress" position="1668,790" size="121,45" zPosition="4" pixmap="'+PATH+'/50/sig-bar36.png" transparent="1" >\n'
g17_extraScreen["50"]  += '<convert type="g17ExtraSource">AgcNum</convert>\n'
g17_extraScreen["50"]  += '</widget>\n'
g17_extraScreen["50"]  += """<widget position="585,684" size="750,39" source="session.CurrentService" render="Label" font="Prive3;30" zPosition="2" valign="top" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    
    <widget name="TP_info" position="277,1011" zPosition="1" size="636,30" font="Prive3;22" halign="center" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="TP_type" position="58,1011" zPosition="1" size="189,30" font="Prive3;22" halign="center" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="Video_size" font="Prive3;27" position="60,684" size="600,39" halign="center" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1672,684" size="183,33" font="Prive3;30" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="g17ClockToText">Format:%H:%M:%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A, %d.%B %Y" position="1041,685" size="660,33" font="Prive3;27" halign="right" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="67,754" size="540,33" font="Prive3;27" halign="center" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" />
    <widget name="bitrate_info" position="1320,754" zPosition="8" size="540,33" font="Prive3;27" halign="center" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1"/>    

    <widget name="Dtype" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    
    <widget name="g17picon" position="660,738" size="600,255" zPosition="2" transparent="1" alphatest="on" />

    <widget position="60,802" size="277,37" source="session.Event_Now" backgroundColor="background" transparent="1" valign="center" render="Label" zPosition="1" font="Prive4;27" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="60,841" size="585,37" source="session.Event_Now" backgroundColor="background" transparent="1" valign="center" render="g17EmptyEpg" readTagInfo="1" zPosition="2" font="Prive4;27" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="375,802" size="277,37" source="session.Event_Now" backgroundColor="background" transparent="1" valign="center" render="Label" zPosition="3" font="Prive4;27"  foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_390.png" position="60,892" size="585,12" zPosition="6" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="60,916" size="0,0" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="5" alphatest="on" />
    <eLabel backgroundColor="white" position="60,898" size="585,1" zPosition="5" /> 
    <widget position="60,916" size="277,37" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="Label" font="Prive4;27"  zPosition="5" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="60,954" size="585,37" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="g17EmptyEpg" font="Prive4;27" zPosition="6" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="375,916" size="277,37" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="Label" font="Prive4;27"  zPosition="7" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1818,919" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1818,919" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1818,919" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1818,919" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1818,919" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1818,919" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1818,919" size="0,0" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1818,919" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1578,838" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>

    <widget name="ecmLineInfo" position="583,997" size="0,0" font="Prive3;22" noWrap="1" halign="right" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" zPosition="5" />

    <eLabel text="Q:" font="Prive3;22" position="1342,801" zPosition="2" size="90,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <eLabel text="S:" font="Prive3;22" position="1644,801" zPosition="2" size="90,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="1494,801" zPosition="5" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" size="90,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="1795,801" zPosition="5" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" size="90,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">AgcText</convert>
    </widget>

    <widget source="session.FrontendInfo" render="g17TunersLabel" font="Regular2;33" alphatest="off" position="1428,838" size="420,37" tuners="12" ActiveTunerColor="#0000d100" backgroundColor="background" BackgroundActiveTunerColor="#00ecb100" zPosition="2"/>  

		<widget name="ecmlabels" font="Prive3;24" position="100,175" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="183,175" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="52,10" size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="112,64" size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="310,64" size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="112,522" size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="310,522" size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,82" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,22"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,82" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,93"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    
  </screen>""" 

g17_extraScreen["51"] = """
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""
g17_extraScreen["51"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/51/infobar-51-fs8.png" alphatest="off" />\n'
g17_extraScreen["51"]  += '<widget  name="back_enhanced" alphatest="off" position="52,25" size="465,601" pixmap="'+PATH+'/51/back_enhanced-51.png" zPosition="0" />\n'
g17_extraScreen["51"]  += '<widget name="caidPids_back" alphatest="off" position="1609,15" size="255,600" pixmap="'+PATH+'/51/back_caidPids-44.png" zPosition="0" />\n'
g17_extraScreen["51"]  += '<widget name="caidPids_end" alphatest="off" position="1609,85" size="255,9" pixmap="'+PATH+'/51/end_caidPids-44.png" zPosition="3" />\n'
g17_extraScreen["51"]  += '<widget source="session.FrontendStatus" render="Progress" position="1366,745" size="121,45" zPosition="4" pixmap="'+PATH+'/51/sig-bar36.png" transparent="1" >\n'
g17_extraScreen["51"]  += '<convert type="g17ExtraSource">SnrNum</convert>\n'                          
g17_extraScreen["51"]  += '</widget>\n'
g17_extraScreen["51"]  += '<widget source="session.FrontendStatus" render="Progress" position="1668,745" size="121,45" zPosition="4" pixmap="'+PATH+'/51/sig-bar36.png" transparent="1" >\n'
g17_extraScreen["51"]  += '<convert type="g17ExtraSource">AgcNum</convert>\n'
g17_extraScreen["51"]  += '</widget>\n'
g17_extraScreen["51"]  += """<widget position="585,639" size="750,39" source="session.CurrentService" render="Label" font="Prive3;30" zPosition="2" valign="top" halign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
            <convert type="ServiceName">Name</convert>
    </widget>
    <widget source="session.CurrentService" render="Label" position="60,639" size="600,39" font="Prive3;30" halign="center" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2" valign="top">
      <convert type="g17ServiceNum">Number</convert>
    </widget>    
    <widget name="TP_info" position="277,966" zPosition="1" size="636,30" font="Prive3;22" halign="center" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="TP_type" position="58,966" zPosition="1" size="189,30" font="Prive3;22" halign="center" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="Video_size" font="Prive3;27" position="1260,793" size="378,72" halign="center" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1672,639" size="183,33" font="Prive3;30" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="g17ClockToText">Format:%H:%M:%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A, %d.%B %Y" position="1041,640" size="660,33" font="Prive3;27" halign="right" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="67,709" size="540,33" font="Prive3;27" halign="center" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" />
    <widget name="bitrate_info" position="1320,709" zPosition="8" size="540,33" font="Prive3;27" halign="center" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1"/>    

    <widget name="Dtype" position="1782,958" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1782,958" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1782,958" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1782,958" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1782,958" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1782,958" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1782,958" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1782,958" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1782,958" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1782,958" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1782,958" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1782,958" size="78,46" zPosition="3" alphatest="off" />
    
    <widget name="g17picon" position="660,693" size="600,255" zPosition="2" transparent="1" alphatest="on" />

    <widget position="60,757" size="277,37" source="session.Event_Now" backgroundColor="background" transparent="1" valign="center" render="Label" zPosition="1" font="Prive4;27" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="60,796" size="585,37" source="session.Event_Now" backgroundColor="background" transparent="1" valign="center" render="g17EmptyEpg" readTagInfo="1" zPosition="2" font="Prive4;27" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="375,757" size="277,37" source="session.Event_Now" backgroundColor="background" transparent="1" valign="center" render="Label" zPosition="3" font="Prive4;27"  foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_390.png" position="60,847" size="585,12" zPosition="6" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="60,916" size="0,0" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="5" alphatest="on" />
    <eLabel backgroundColor="white" position="60,853" size="585,1" zPosition="5" /> 
    <widget position="60,871" size="277,37" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="Label" font="Prive4;27"  zPosition="5" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="60,909" size="585,37" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="g17EmptyEpg" font="Prive4;27" zPosition="6" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="375,871" size="277,37" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="Label" font="Prive4;27"  zPosition="7" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1818,874" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1818,874" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1818,874" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1818,874" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1818,874" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1818,874" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1818,874" size="0,0" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1818,874" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1578,793" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>

    <widget name="ecmLineInfo" position="0,1012" size="1920,45" font="Prive3;22" noWrap="1" halign="center" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" zPosition="5" />

    <eLabel text="Q:" font="Prive3;22" position="1342,756" zPosition="2" size="90,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <eLabel text="S:" font="Prive3;22" position="1644,756" zPosition="2" size="90,30" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="1494,756" zPosition="5" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" size="90,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="1795,756" zPosition="5" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" size="90,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">AgcText</convert>
    </widget>

    <widget source="session.FrontendInfo" render="g17TunersLabel" alphatest="off" font="Regular2;33" position="1638,793" size="210,75" tuners="12" ActiveTunerColor="#0000d100" backgroundColor="background" BackgroundActiveTunerColor="#00ecb100" zPosition="2"/>  

		<widget name="ecmlabels" font="Prive3;24" position="100,160" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="183,160" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="picProv" position="112,49" size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="310,49" size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="112,509" size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="310,509" size="150,90"  zPosition="2" alphatest="on"/>

    <widget  name="caidPids" transparent="1" position="1639,75" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="active_caidPid" transparent="1" position="1639,75" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    
  </screen>""" 
g17_extraScreen["52"] = """

    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <widget source="session.FrontendStatus" render="Label" font="Prive4;22" position="1429,756" zPosition="2" size="198,33" valign="center" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" >
    <convert type="g17ExtraSource">SnrAgcTxt</convert>
    </widget>

    <widget source="session.FrontendInfo" render="g17TunersLabel" alphatest="on" font="Regular2;27" position="1417,717" size="247,30" tuners="10" ActiveTunerColor="#0000d100" backgroundColor="#00000000" BackgroundActiveTunerColor="#00ecb100" zPosition="2"/>""" 
                    
g17_extraScreen["52"]  += '<ePixmap position="81,681" size="432,138" pixmap="'+PATH+'/52/tab1.png" zPosition="1" alphatest="on" />\n' 
g17_extraScreen["52"]  += '<ePixmap position="1398,681" size="432,138" pixmap="'+PATH+'/52/tab1.png" zPosition="1" alphatest="on" />\n'    
g17_extraScreen["52"]  += """<widget position="100,709" size="390,81" source="session.CurrentService" render="Label" font="Prive4;30" zPosition="2" valign="center" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
   
    <widget name="bitrate_info" position="771,798" zPosition="6" size="597,33" font="Prive4;24" noWrap="1" valign="center" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" />
    <widget name="ecmLineInfo" position="663,1017" size="1182,24" font="Prive4;21" noWrap="1" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" zPosition="5" transparent="1" />

    <widget name="TP_info" position="537,760" zPosition="6" size="840,34" font="Prive4;24" noWrap="1" halign="center" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget name="TP_type" position="546,798" zPosition="6" size="225,33" font="Prive4;24" halign="left" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget name="Video_size" font="Prive4;24" position="735,798" size="225,33" zPosition="6" halign="center" valign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
  
    <widget source="global.CurrentTime" render="g17dateFormat" format="%d.%m.%Y" position="1660,756" size="142,33" font="Prive4;22" zPosition="2"  valign="center" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1660,709" size="105,40" font="Prive4;31" zPosition="2"  valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1767,712" size="60,33" font="Prive4;22" zPosition="2"  valign="top" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>

    <widget name="Prov_temp_rpm" position="64,1017" size="603,24" font="Prive4;22" halign="left" backgroundColor="background" transparent="1" foregroundColor="un99bad6" zPosition="5" />

    <widget name="Dtype" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    
    <widget name="g17picon" position="760,544" size="400,170" zPosition="2" transparent="1" alphatest="on" />
    
    <widget position="162,846" size="120,57" source="session.Event_Now" backgroundColor="background" transparent="1" valign="center" render="Label" zPosition="8" font="Prive4;33" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="288,846" size="567,57" source="session.Event_Now" backgroundColor="background" transparent="1" valign="center" render="g17EmptyEpg" readTagInfo="1" zPosition="7" font="Prive4;34"  noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="855,846" size="157,57" source="session.Event_Now" backgroundColor="background" transparent="1" valign="center" render="Label" zPosition="6" font="Prive4;31"  foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slidermain.png" position="177,900" size="837,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="177,900" size="0,0" pixmap="hd_glass17/slider/sliderback-fs8.png" zPosition="2" alphatest="on" />
    <eLabel backgroundColor="white" position="177,910" size="837,1" zPosition="2" />  
    <widget position="162,925" size="120,45" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="Label" font="Prive4;33"  zPosition="8" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="288,925" size="582,45" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="g17EmptyEpg" font="Prive4;34"  zPosition="7" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="870,925" size="142,45" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="Label" font="Prive4;31"  zPosition="6" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    
    <widget name="subserv" position="1713,852" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1713,852" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1713,852" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1713,852" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1713,852" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1713,852" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1713,852" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1713,852" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1713,852" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
		<widget name="ecmlabels" font="Prive3;24" position="108,172" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,172" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="picProv" position="120,61"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,61"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,519"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,519"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />"""
g17_extraScreen["52"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/52/infobar-1x.png" alphatest="off" />\n' 
g17_extraScreen["52"]  += '<ePixmap position="746,534" size="426,192" zPosition="1" pixmap="'+PATH+'/52/FrameZ.png" transparent="1" alphatest="on" />\n'
g17_extraScreen["52"]  += '<widget  name="back_enhanced" alphatest="off" position="60,7"  size="465,660" pixmap="'+PATH+'/52/back_enhanced25-fs8.png" zPosition="0" />\n'
g17_extraScreen["52"]  += '<widget name="caidPids_back" alphatest="off" position="1609,45"  size="255,600" pixmap="'+PATH+'/52/back_caidPidsX-fs8.png" zPosition="0" />\n'
g17_extraScreen["52"]  += '<widget name="caidPids_end" alphatest="off" position="1609,115"  size="255,30" pixmap="'+PATH+'/52/end_caidPids26-fs8.png" zPosition="3" />\n'    
g17_extraScreen["52"]  += """</screen>"""                    

g17_extraScreen["53"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <widget position="100,709" size="390,81" source="session.CurrentService" render="Label" font="Prive4;36" zPosition="2" valign="center" halign="center" foregroundColor="#ffcc00" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
   
    <widget name="bitrate_info" position="771,798" zPosition="6" size="597,33" font="Prive4;24" noWrap="1" valign="center" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" />
    <widget name="ecmLineInfo" position="663,1017" size="1182,24" font="Prive4;21" noWrap="1" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" zPosition="5" transparent="1" />

    <widget name="TP_info" position="537,760" zPosition="6" size="840,34" font="Prive4;24" noWrap="1" halign="center" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget name="TP_type" position="546,798" zPosition="6" size="225,33" font="Prive4;24" halign="left" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget name="Video_size" font="Prive4;24" position="735,798" size="225,33" zPosition="6" halign="center" valign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
  
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="1435,799" size="373,30" font="Prive4;22" valign="center" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget source="session.FrontendStatus" render="g17Ahours" position="1480,661" size="108,108" zPosition="3" foregroundColor="white" alphatest="on">
		<convert type="g17ExtraSource">SnrAnalog</convert>
		</widget>    
    <widget source="session.FrontendStatus" render="Label" font="Prive4;22" position="1488,727" zPosition="4" backgroundColor="black" size="90,28" valign="center" halign="center" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
  
		<widget source="global.CurrentTime" render="g17Ahours" position="1654,661" size="108,108" zPosition="4" alphatest="on" foregroundColor="#f23d21">
			<convert type="g17ExtraSource">secHand</convert>
		</widget>
		<widget source="global.CurrentTime" render="g17Ahours" position="1663,670" size="90,90" zPosition="3" foregroundColor="white" alphatest="on">
			<convert type="g17ExtraSource">minHand</convert>
		</widget>
		<widget source="global.CurrentTime" render="g17Ahours" position="1674,681" size="69,69" zPosition="2" foregroundColor="white" alphatest="on">
			<convert type="g17ExtraSource">hourHand</convert>
		</widget>

    <widget name="Prov_temp_rpm" position="64,1017" size="603,24" font="Prive4;22" halign="left" backgroundColor="background" transparent="1" foregroundColor="un99bad6" zPosition="5" />

    <widget name="Dtype" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1675,924" size="78,46" zPosition="3" alphatest="off" />
    
    <widget name="g17picon" position="760,544" size="400,170" zPosition="2" transparent="1" alphatest="on" />
    
    <widget position="162,846" size="120,57" source="session.Event_Now" backgroundColor="background" transparent="1" valign="center" render="Label" zPosition="8" font="Prive4;33" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="288,846" size="424,57" source="session.Event_Now" backgroundColor="background" transparent="1" valign="center" render="g17EmptyEpg" readTagInfo="1" zPosition="7" font="Prive4;34"  noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="712,846" size="157,57" source="session.Event_Now" backgroundColor="background" transparent="1" valign="center" render="Label" zPosition="6" font="Prive4;31"  foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slidermain.png" position="177,900" size="694,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="177,900" size="0,0" pixmap="hd_glass17/slider/sliderback-fs8.png" zPosition="2" alphatest="on" />
    <eLabel backgroundColor="white" position="177,910" size="694,1" zPosition="2" />  
    <widget position="162,925" size="120,45" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="Label" font="Prive4;33"  zPosition="8" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="288,925" size="439,45" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="g17EmptyEpg" font="Prive4;34"  zPosition="7" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="727,925" size="142,45" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="Label" font="Prive4;31"  zPosition="6" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    
    <widget name="subserv" position="1713,852" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1713,852" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1713,852" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1713,852" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1713,852" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1713,852" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1713,852" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1713,852" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1713,852" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
		<widget name="ecmlabels" font="Prive3;24" position="108,172" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,172" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="picProv" position="120,61"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,61"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,519"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,519"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget source="session.CurrentService" render="g17PicRef" position="885,861" size="150,90" zPosition="2" transparent="1" alphatest="on">
      <convert type="ServiceName">Reference</convert>
    </widget>""" 
g17_extraScreen["53"]  += '<ePixmap position="81,681" size="432,138" pixmap="'+PATH+'/53/tab1.png" zPosition="1" alphatest="on" />\n' 
g17_extraScreen["53"]  += '<ePixmap position="746,534" size="426,192" zPosition="1" pixmap="'+PATH+'/53/FrameZ.png" transparent="1" alphatest="on" />\n'
g17_extraScreen["53"]  += '<ePixmap position="871,840" size="175,138" pixmap="'+PATH+'/53/tab2.png" zPosition="1" alphatest="on" />\n'
g17_extraScreen["53"]  += '<ePixmap position="1471,652" size="127,127" pixmap="'+PATH+'/53/sig-30-fs8.png" zPosition="1" alphatest="on" />\n'
g17_extraScreen["53"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/53/infobar-2x.png" alphatest="off" />\n' 
g17_extraScreen["53"]  += '<widget  name="back_enhanced" alphatest="off" position="60,7"  size="465,660" pixmap="'+PATH+'/53/back_enhanced25-fs8.png" zPosition="0" />\n'
g17_extraScreen["53"]  += '<widget name="caidPids_back" alphatest="off" position="1609,45"  size="255,600" pixmap="'+PATH+'/53/back_caidPidsX-fs8.png" zPosition="0" />\n'
g17_extraScreen["53"]  += '<widget name="caidPids_end" alphatest="off" position="1609,115"  size="255,30" pixmap="'+PATH+'/53/end_caidPids26-fs8.png" zPosition="3" />\n'    
g17_extraScreen["53"]  += """</screen>"""

g17_extraScreen["54"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="hd_glass17/general/infobar-ex.png" alphatest="off" />

    <widget position="120,756" size="900,54" source="session.CurrentService" render="Label" font="Prive4;48" valign="center" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%d.%m.%Y" position="1275,753" size="270,60" font="Prive4;42" valign="center" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1560,753" size="270,60" font="Prive4;54" valign="center" halign="right" backgroundColor="un353e575e" foregroundColor="yellow" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format:%H:%M:%S</convert>
    </widget>
    <ePixmap position="90,847" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="109,864" size="150,90" zPosition="2" transparent="1" alphatest="on" />   
  
    <widget position="270,832" size="180,66" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" font="Prive4;48" valign="center" halign="right" foregroundColor="green">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="472,832" size="1129,66" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" font="Prive4;54" valign="center" noWrap="1" foregroundColor="green">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1597,825" size="225,66" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" font="Prive4;42" valign="center" foregroundColor="green" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main4.png" position="472,903" size="1129,15" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="472,903" size="1129,15" pixmap="hd_glass17/slider/slider_back4.png" zPosition="2" alphatest="on" />    
    <widget position="270,922" size="180,60" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;42" valign="center" halign="right" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="472,922" size="1129,60" source="session.Event_Next" render="g17EmptyEpg" transparent="1" backgroundColor="background" font="Prive4;42" valign="center" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1590,922" size="225,60" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;42" valign="center" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="ecmLineInfo" position="90,987" zPosition="1" size="1350,30" font="Prive4;24" halign="right" valign="top" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />
  
    <eLabel text="Snr:" font="Prive4;27" position="1477,987" size="60,33" foregroundColor="green" transparent="1" valign="top" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="1545,987" size="97,33" transparent="1" font="Prive4;27" valign="top" zPosition="1" backgroundColor="background" foregroundColor="white">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="1657,987" size="67,33" font="Prive4;27" foregroundColor="yellow" transparent="1" valign="top" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="1732,987" size="97,33" transparent="1" font="Prive4;27" valign="top" backgroundColor="background" foregroundColor="white">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>

    <widget name="subserv" position="1597,871" size="0,0" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1597,871" size="0,0" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1597,871" size="0,0" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1597,871" size="0,0" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1597,871" size="0,0" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="0,0" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="0,0" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="0,0" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1597,871" size="0,0" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1597,871" size="0,0" zPosition="1" alphatest="off" />          
    <widget name="TP_type" position="121,951" zPosition="1" size="0,0" font="Prive4;24" halign="left" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />
    <widget name="TP_info" position="315,951" zPosition="1" size="0,0" font="Prive4;24" halign="center" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />
    <widget name="Dtype" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1723,951" size="0,0" zPosition="3" alphatest="off" />   
    <widget name="bitrate_info" position="1377,991" zPosition="8" size="0,0" font="Prive3;27" halign="left" backgroundColor="background" foregroundColor="red" transparent="1"/>
		<widget name="ecmlabels" font="Prive3;24" position="100,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="183,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="52,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="112,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="310,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="112,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="310,572"  size="150,90"  zPosition="2" alphatest="on"/> 
    <widget  name="caidPids" transparent="1" position="529,157" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="499,97"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="-1" />  	 	
    <widget name="active_caidPid" transparent="1" position="529,157" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="499,163"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />

	</screen>"""

g17_extraScreen["55"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="hd_glass17/general/infobar-ex55.png" alphatest="off" />

    <widget position="120,663" size="900,54" source="session.CurrentService" render="Label" font="Prive4;48" valign="center" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%d.%m.%Y" position="1275,660" size="270,60" font="Prive4;42" valign="center" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1560,660" size="270,60" font="Prive4;54" valign="center" halign="right" backgroundColor="un353e575e" foregroundColor="yellow" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format:%H:%M:%S</convert>
    </widget>
    <ePixmap position="108,757" size="426,192" zPosition="1" pixmap="hd_glass17/frame/FrameZ.png" transparent="1" alphatest="on" />
    <widget name="g17picon" position="121,768" size="400,170" zPosition="2" transparent="1" alphatest="on" />  
  
    <widget position="597,760" size="180,66" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" font="Prive4;48" valign="center" halign="left" foregroundColor="green">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="762,760" size="819,66" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" font="Prive4;54" valign="center" noWrap="1" foregroundColor="green">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1577,760" size="225,66" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" font="Prive4;42" valign="center" foregroundColor="green" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main4.png" position="655,850" size="1129,15" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="627,850" size="1129,15" pixmap="hd_glass17/slider/slider_back4.png" zPosition="2" alphatest="on" />    
    <widget position="597,892" size="180,60" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;42" valign="center" halign="left" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="762,892" size="819,60" source="session.Event_Next" render="g17EmptyEpg" transparent="1" backgroundColor="background" font="Prive4;42" valign="center" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1570,892" size="225,60" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;42" valign="center" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="ecmLineInfo" position="90,987" zPosition="1" size="1350,30" font="Prive4;24" halign="right" valign="top" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />
  
    <eLabel text="Snr:" font="Prive4;27" position="1477,987" size="60,33" foregroundColor="green" transparent="1" valign="top" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="1545,987" size="97,33" transparent="1" font="Prive4;27" valign="top" zPosition="1" backgroundColor="background" foregroundColor="white">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="1657,987" size="67,33" font="Prive4;27" foregroundColor="yellow" transparent="1" valign="top" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="1732,987" size="97,33" transparent="1" font="Prive4;27" valign="top" backgroundColor="background" foregroundColor="white">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>

    <widget name="subserv" position="1597,871" size="0,0" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1597,871" size="0,0" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1597,871" size="0,0" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1597,871" size="0,0" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1597,871" size="0,0" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="0,0" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="0,0" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="0,0" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1597,871" size="0,0" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1597,871" size="0,0" zPosition="1" alphatest="off" />          
    <widget name="TP_type" position="121,951" zPosition="1" size="0,0" font="Prive4;24" halign="left" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />
    <widget name="TP_info" position="315,951" zPosition="1" size="0,0" font="Prive4;24" halign="center" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />
    <widget name="Dtype" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1723,951" size="0,0" zPosition="3" alphatest="off" />   
    <widget name="bitrate_info" position="1377,991" zPosition="8" size="0,0" font="Prive3;27" halign="left" backgroundColor="background" foregroundColor="red" transparent="1"/>
		<widget name="ecmlabels" font="Prive3;24" position="100,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="183,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="52,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="112,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="310,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="112,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="310,572"  size="150,90"  zPosition="2" alphatest="on"/> 
    <widget  name="caidPids" transparent="1" position="529,157" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="499,97"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="-1" />  	 	
    <widget name="active_caidPid" transparent="1" position="529,157" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="499,163"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />

	</screen>"""

g17_extraScreen["56"] = """                                      
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""
g17_extraScreen["56"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/56/infobar-46-fs8.png" alphatest="off" />\n'
g17_extraScreen["56"]  += '<ePixmap pixmap="'+PATH+'/56/snr-all.png" position="1612,727" size="192,114" zPosition="1" alphatest="off"/>\n'
g17_extraScreen["56"]  += '<ePixmap pixmap="'+PATH+'/56/snr-b.png" position="1686,823" size="46,21" zPosition="4" alphatest="off"/>\n'
g17_extraScreen["56"]  += """<widget position="675,684" size="637,39" source="session.CurrentService" render="Label" font="Prive3;30" zPosition="2" valign="top" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="1545,747" zPosition="2" backgroundColor="background" size="105,24" halign="right" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="1774,747" zPosition="2" backgroundColor="background" size="120,24" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrdB</convert>
    </widget>
		<widget source="session.FrontendStatus" render="g17Ahours" position="1632,765" size="150,150" zPosition="3" foregroundColor="yellow" alphatest="on">
		<convert type="g17ExtraSource">SnrAnalog</convert>
		</widget>    
    <widget source="session.FrontendInfo" render="g17TunersLabel" font="Regular2;33" alphatest="off" position="1552,870" size="315,37" tuners="12" ActiveTunerColor="#0000d100" backgroundColor="background" BackgroundActiveTunerColor="#00ecb100" zPosition="2"/>  
        
    <widget name="TP_info" position="277,1011" zPosition="1" size="636,30" font="Prive3;22" halign="center" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="TP_type" position="58,1011" zPosition="1" size="189,30" font="Prive3;22" halign="center" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="Video_size" font="Prive3;27" position="60,684" size="600,39" halign="center" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1672,684" size="183,33" font="Prive3;30" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1">
      <convert type="g17ClockToText">Format:%H:%M:%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A, %d.%B %Y" position="1041,685" size="660,33" font="Prive3;27" halign="right" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="681,898" size="540,33" font="Prive3;27" halign="center" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" />
    <widget name="bitrate_info" position="681,949" zPosition="8" size="540,33" font="Prive3;27" halign="center" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1"/>    

    <widget name="Dtype" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1782,1003" size="78,46" zPosition="3" alphatest="off" />
    
    <widget name="g17picon" position="60,738" size="600,255" zPosition="2" transparent="1" alphatest="on" />

    <widget position="675,783" size="105,45" source="session.Event_Now" render="Label" zPosition="1" font="Prive3;34" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="780,783" size="783,45" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive3;36" valign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1">
      <convert type="EventName">Name</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="780,753" size="762,21" zPosition="6" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="780,753" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="5" alphatest="on" />

    <widget position="675,835" size="105,45" source="session.Event_Next" render="Label" font="Prive3;34" valign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="780,835" size="783,45" source="session.Event_Next" render="g17EmptyEpg" font="Prive3;36" valign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1">
      <convert type="EventName">Name</convert>
    </widget>

    <widget name="subserv" position="1818,919" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1818,919" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1818,919" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1818,919" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1818,919" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1818,919" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1818,919" size="0,0" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1818,919" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1578,838" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>

    <widget name="ecmLineInfo" position="583,997" size="0,0" font="Prive3;22" noWrap="1" halign="right" valign="top" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" zPosition="5" />

		<widget name="ecmlabels" font="Prive3;24" position="100,175" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="183,175" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="52,10" size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="112,64" size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="310,64" size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="112,522" size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="310,522" size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,82" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,22"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,82" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,93"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    
  </screen>"""
   
g17_extraScreen["57"] = """
                                             
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
<ePixmap position="0,761" zPosition="-2" size="1920,495" pixmap="hd_glass17/general/infobar-57.png" alphatest="off" />

	  <widget source="session.CurrentService" render="Label" position="265,809" size="1050,48" font="Prive4;38" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">	
    <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <eLabel position="70,979" zPosition="8" size="1780,1" backgroundColor="#1546AF" transparent="0" />

    <widget name="TP_type" position="72,990" zPosition="1" size="293,30" font="Prive4;24" halign="left" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />
    <widget name="TP_info" position="268,990" zPosition="2" size="850,30" font="Prive4;24" halign="left" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />
    <widget name="Video_size" font="Prive3;27" position="65,822" size="180,33" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1659,809" size="135,48" font="Prive4;38" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1775,811" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="996,822" size="660,33" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="1026,859" size="630,37" font="Prive4;27" halign="right" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

    <widget name="Dtype" position="1773,987" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1773,987" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1773,987" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1773,987" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1773,987" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1773,987" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1773,987" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1773,987" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1773,987" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1773,987" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1773,987" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1773,987" size="78,46" zPosition="3" alphatest="off" />
        
    <ePixmap position="61,856" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="80,872" size="150,90" zPosition="2" transparent="1" alphatest="on" />

    <widget position="265,890" size="90,39" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="361,890" size="595,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="981,890" size="142,39" source="session.Event_Now" render="Label" zPosition="1" backgroundColor="background" transparent="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider57.png" position="263,864" size="862,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="263,864" size="862,21" pixmap="hd_glass17/slider/slider_back57.png" zPosition="2" alphatest="blend" />

    <widget position="265,929" size="90,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="361,929" size="595,39" source="session.Event_Next" render="g17EmptyEpg" backgroundColor="background" transparent="1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="981,929" size="142,39" source="session.Event_Next" render="Label" backgroundColor="background" transparent="1" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    <ePixmap position="1670,856" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1689,872" size="150,90" zPosition="2" transparent="1" alphatest="on" />
    <widget name="weaTxt" position="1689,872" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />

    <widget name="subserv" position="1619,905" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1619,905" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1619,905" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1619,905" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1619,905" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1619,905" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1619,905" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1619,905" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1619,905" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1619,905" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1619,905" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>    
    <widget name="ecmLineInfo" position="730,1030" size="1117,24" font="Prive4;18" noWrap="1" halign="right" transparent="1" backgroundColor="background" foregroundColor="unb2e0b4" zPosition="5" />
    <eLabel text="Snr: dB" font="Prive4;24" position="73,1024" size="105,30" foregroundColor="un99bad6" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="176,1024" size="90,30" font="Prive4;24" transparent="1" backgroundColor="background" zPosition="5" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">SnrdB</convert>
    </widget>
    <eLabel text="Snr:" position="269,1024" size="60,30" font="Prive4;24" foregroundColor="un99bad6" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="329,1024" size="90,30" transparent="1" backgroundColor="background" font="Prive4;24" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="419,1024" size="60,30" font="Prive4;24" foregroundColor="un99bad6" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="479,1024" size="90,30" transparent="1" backgroundColor="background" font="Prive4;24" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <eLabel text="Ber:" position="569,1024" size="60,30" font="Prive4;24" foregroundColor="un99bad6" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="629,1024" size="90,30" transparent="1" backgroundColor="background" font="Prive4;24" foregroundColor="unefb2b2">
      <convert type="g17ExtraSource">BerText</convert>
    </widget>
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="caidPids" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" transparent="1" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    
  </screen>"""
  
g17_extraScreen["58"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <ePixmap position="0,80" zPosition="-2" size="1920,1080" pixmap="hd_glass17/general/infobar-ex.png" alphatest="off" />

  	<widget name="Video_size" font="Prive4;28" position="100,846" size="217,33" halign="center" backgroundColor="lightblue" transparent="1" />

    <widget position="315,837" size="757,48" source="session.CurrentService" render="Label" font="Prive4;37" valign="bottom" halign="left" noWrap="1" backgroundColor="black" foregroundColor="red" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="937,842" size="660,30" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1609,837" size="135,48" font="Prive4;36" valign="top" halign="right" backgroundColor="black" foregroundColor="red" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1725,840" size="69,34" font="Prive4;30" valign="top" halign="right" backgroundColor="black" foregroundColor="blue" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <ePixmap position="101,904" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="120,920" size="150,90" zPosition="2" transparent="1" alphatest="on" />   
  
    <widget name="Prov_temp_rpm" position="1027,912" size="607,37" font="Prive4;27" halign="right" transparent="1" backgroundColor="background" foregroundColor="un99bad6" />

    <ePixmap position="1635,904" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1654,920" size="150,90" zPosition="2" transparent="1" alphatest="blend" />    
    <widget name="weaTxt" position="1654,920" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
    
    <widget position="310,908" size="112,39" source="session.Event_Now" render="Label" zPosition="1" transparent="1" backgroundColor="background" font="Prive4;31" valign="bottom" foregroundColor="green">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="421,908" size="495,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="-1" font="Prive4;31" valign="bottom" noWrap="1" foregroundColor="yellow">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="904,908" size="150,39" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" zPosition="1" font="Prive4;31" valign="bottom" foregroundColor="green" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="308,956" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="308,956" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />    
    <widget position="310,984" size="112,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;31" valign="bottom" foregroundColor="yellow">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="421,984" size="495,39" source="session.Event_Next" render="g17EmptyEpg" transparent="1" backgroundColor="background" font="Prive4;31" valign="bottom" noWrap="1" foregroundColor="green">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="904,984" size="150,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;31" valign="bottom" foregroundColor="yellow" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1597,951" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1597,951" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1597,951" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1597,951" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1597,951" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,951" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,951" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,951" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1597,951" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1597,951" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1597,951" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
        
    <ePixmap position="120,1032" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="960,1032" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />

    <widget name="Dtype" position="1734,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1734,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1734,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="0,0" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1734,944" size="0,0" zPosition="3" alphatest="off" />
  	
		<widget name="ecmlabels" font="Prive3;24" position="100,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="183,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="52,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="112,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="310,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="112,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="310,572"  size="150,90"  zPosition="2" alphatest="on"/> 
    <widget  name="caidPids" transparent="1" position="529,157" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="499,97"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="-1" />  	 	
    <widget name="active_caidPid" transparent="1" position="529,157" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="499,163"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />

	</screen>"""

g17_extraScreen["59"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="hd_glass17/general/infobar-99.png" alphatest="off" />

  	<widget name="Video_size" font="Prive4;27" position="100,766" size="210,31" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />

    <widget source="session.CurrentService" render="Label" position="315,754" size="877,48" font="Prive4;39" halign="left" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2" valign="bottom">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="937,766" size="660,30" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1609,754" size="135,48" font="Prive4;39" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1725,757" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <ePixmap position="111,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="130,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />   
  
    <widget name="Prov_temp_rpm" position="1075,826" size="525,33" font="Prive3;27" halign="right" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

    <ePixmap position="1620,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1639,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />    
    <widget name="weaTxt" position="1639,835" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
    
    <widget position="315,828" size="90,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,828" size="495,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,828" size="142,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" halign="right" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="313,872" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="313,872" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />    
    <widget position="315,892" size="90,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,892" size="495,39" source="session.Event_Next" render="g17EmptyEpg" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6" transparent="1" backgroundColor="background">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,892" size="142,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" halign="right" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1569,871" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1569,871" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1569,871" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
    <ePixmap position="120,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="960,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <widget name="TP_type" position="121,952" zPosition="2" size="293,30" font="Prive4;22" halign="left" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget name="TP_info" position="315,951" zPosition="1" size="735,30" font="Prive4;24" halign="center" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />

    <widget name="Dtype" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
          	
    <eLabel text="Snr:" font="Prive4;20" position="121,998" size="60,30" halign="left" foregroundColor="un99bad6" transparent="1" backgroundColor="background"/>
    <widget source="session.FrontendStatus" render="Label" position="185,998" size="105,30" font="Prive4;20" halign="left" zPosition="5" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17ExtraSource">SnrdB2</convert>
    </widget>
    <ePixmap pixmap="hd_glass17/slider/sigsnrbar_back43.png" position="121,988" size="230,6" zPosition="1" alphatest="on"/>
  	<widget source="session.FrontendStatus" render="Progress" position="121,988" size="230,6" zPosition="2" pixmap="hd_glass17/slider/sigbar43.png" transparent="1" >
    <convert type="g17ExtraSource">SnrNum</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" position="246,998" size="105,30" font="Prive4;20" halign="right" zPosition="5" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>

    <widget name="bitrate_info" position="375,998" zPosition="4" size="400,30" font="Prive4;20" halign="left" backgroundColor="background" transparent="1"/>    
    <widget name="ecmLineInfo" position="639,994" size="1158,24" font="Prive4;18" noWrap="1" halign="right" backgroundColor="background" foregroundColor="unb2e0b4" zPosition="5" transparent="1" />
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>	
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    </screen>"""
    	
g17_extraScreen["60"] = """
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""
g17_extraScreen["60"]  += '<ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="'+PATH+'/60/infobar-35-fs8.png" alphatest="off" />\n'
g17_extraScreen["60"]  += """
    <widget position="283,772" size="757,52" source="session.CurrentService" render="Label" font="Prive4;39" zPosition="2" valign="top" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <ePixmap position="90,957" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="930,957" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="982,957" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <widget name="TP_info" position="288,966" zPosition="1" size="750,30" font="Prive3;24" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="TP_type" position="91,966" zPosition="2" size="293,30" font="Prive3;22" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1" />
    <widget name="Video_size" font="Prive4;27" position="85,781" size="180,33" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1639,769" size="135,48" font="Prive4;39" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1755,772" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="967,781" size="660,33" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />

    <widget name="Prov_temp_rpm" position="1090,841" size="547,37" font="Prive4;27" halign="right" backgroundColor="background" transparent="1" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1431,966" size="78,46" zPosition="1" alphatest="off" />
    <widget name="Dcam" position="1431,966" size="78,46" zPosition="1" alphatest="off" />
    <widget name="Decm" position="1431,966" size="78,46" zPosition="1" alphatest="off" />
    <widget name="Dnetstate" position="1431,966" size="78,46" zPosition="1" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1431,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1431,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1431,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1431,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1431,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1480,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1431,966" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1431,966" size="78,46" zPosition="3" alphatest="off" />
    
    <widget source="session.FrontendInfo" render="g17TunersLabel" alphatest="off" PosLR="R" font="Regular2;31" position="1572,971" size="250,39" tuners="10" ActiveTunerColor="#0000d100" backgroundColor="background" BackgroundActiveTunerColor="#00ecb100" zPosition="2"/>  

    <ePixmap position="81,834" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="100,850" size="150,90" zPosition="2" transparent="1" alphatest="on" />

    <widget position="285,873" size="90,39" source="session.Event_Now" backgroundColor="background" transparent="1" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="381,873" size="555,39" source="session.Event_Now" backgroundColor="background" transparent="1" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="939,873" size="142,39" source="session.Event_Now" backgroundColor="background" transparent="1" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="313,837" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="313,837" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />
    <widget position="285,907" size="90,39" source="session.Event_Next" backgroundColor="background" transparent="1" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="381,907" size="555,39" source="session.Event_Next" backgroundColor="background" transparent="1" render="g17EmptyEpg" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="939,907" size="142,39" source="session.Event_Next" backgroundColor="background" transparent="1" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    <widget name="subserv" position="1606,886" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1606,886" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1606,886" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1606,886" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1606,886" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1606,886" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1606,886" size="0,0" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1606,886" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1092,886" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
    <widget name="bitrate_info" position="91,1003" zPosition="8" size="750,30" font="Prive3;24" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,0" transparent="1"/>    
    <widget name="ecmLineInfo" position="813,1014" size="1018,24" font="Prive4;18" noWrap="1" halign="right" backgroundColor="background" transparent="1" foregroundColor="unb2e0b4" zPosition="5" />

    <widget source="session.FrontendStatus" render="Progress" position="1672,834" size="7,112" zPosition="4" pixmap="hd_glass17/icons/bar.png" orientation="orBottomToTop" transparent="1" >
    <convert type="g17ExtraSource">SnrNum</convert>                          
    </widget>
    <widget source="session.FrontendStatus" render="Progress" position="1815,834" size="7,112" zPosition="4" pixmap="hd_glass17/icons/bar.png" orientation="orBottomToTop" transparent="1" >
    <convert type="g17ExtraSource">AgcNum</convert>
    </widget>

    <ePixmap pixmap="hd_glass17/icons/bar_back_snr.png" position="1672,834" size="7,112" zPosition="1" alphatest="on"/>
    <ePixmap pixmap="hd_glass17/icons/bar_back.png" position="1815,834" size="7,112" zPosition="1" alphatest="on"/>

    <eLabel text="Snr:" font="Prive3;22" position="1692,834" zPosition="2" size="142,30" halign="left" backgroundColor="background" foregroundColor="green" transparent="1" />
    <eLabel text="Agc:" font="Prive3;22" position="1692,876" zPosition="2" size="142,30" halign="left" backgroundColor="background" foregroundColor="yellow" transparent="1" />
    <eLabel text="Ber:" font="Prive3;22" position="1692,918" zPosition="4" size="142,30" halign="left" backgroundColor="background" foregroundColor="red" transparent="1" />

    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="1744,834" zPosition="5" backgroundColor="background" foregroundColor="white" size="105,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="1744,876" zPosition="5" backgroundColor="background" foregroundColor="white" size="105,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;22" position="1744,918" zPosition="5" backgroundColor="background" foregroundColor="white" size="105,30" halign="left" transparent="1"  >
    <convert type="g17ExtraSource">BerText</convert> 
    </widget>

		<widget name="ecmlabels" font="Prive3;24" position="108,210" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,210" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,45"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,99"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,99"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,556"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,556"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,90" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,90" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    
  </screen>"""

g17_extraScreen["61"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="hd_glass17/general/infobar-ex.png" alphatest="off" />

  	<widget name="Video_size" font="Prive4;27" position="100,766" size="210,31" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />

    <widget source="session.CurrentService" render="Label" position="315,754" size="877,48" font="Prive4;39" halign="left" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2" valign="bottom">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="937,766" size="660,30" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1609,754" size="135,48" font="Prive4;39" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1725,757" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <ePixmap position="111,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="130,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />   
  
    <widget name="Prov_temp_rpm" position="1075,826" size="525,33" font="Prive3;27" halign="right" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

    <ePixmap position="1620,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="1639,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />    
    <widget name="weaTxt" position="1639,835" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
    
    <widget position="315,828" size="90,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,828" size="495,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,828" size="142,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" halign="right" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="313,867" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="313,867" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />    
    <widget position="315,892" size="90,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="411,892" size="495,39" source="session.Event_Next" render="g17EmptyEpg" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6" transparent="1" backgroundColor="background">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,892" size="142,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" halign="right" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1569,871" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1569,871" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1569,871" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
    <ePixmap position="120,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="960,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <widget name="TP_type" position="121,952" zPosition="2" size="293,30" font="Prive4;22" halign="left" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget name="TP_info" position="315,951" zPosition="1" size="735,30" font="Prive4;24" halign="center" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />

    <widget name="Dtype" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1723,951" size="78,46" zPosition="3" alphatest="off" />
          	
  	<widget source="session.FrontendStatus" render="Progress" position="178,1002" size="230,6" zPosition="2" pixmap="hd_glass17/slider/sigbar43.png" transparent="1" >
    <convert type="g17ExtraSource">SnrNum</convert>
    </widget>
    <ePixmap pixmap="hd_glass17/slider/sigsnrbar_back43.png" position="178,1002" size="230,6" zPosition="1" alphatest="on"/>
    <eLabel text="Snr:" font="Prive4;24" position="121,988" size="60,30" halign="left" foregroundColor="green" transparent="1" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="416,988" size="80,33" halign="left" transparent="1" font="Prive4;24" zPosition="1" backgroundColor="background" foregroundColor="white">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Snr:" position="506,988" size="60,30" font="Prive4;24" halign="left" foregroundColor="yellow" transparent="1" backgroundColor="background" />
        <widget source="session.FrontendStatus" render="Label" font="Prive4;24" position="564,988" zPosition="5" size="175,30" halign="left" backgroundColor="background" foregroundColor="white" transparent="1" >
        <convert type="g17ExtraSource">SnrdB2</convert>
        </widget>
    <widget name="ecmLineInfo" position="780,994" size="1017,24" font="Prive4;18" noWrap="1" halign="right" backgroundColor="background" foregroundColor="unb2e0b4" zPosition="5" transparent="1" />
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>	
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />

	</screen>"""
	
g17_extraScreen["62"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <eLabel position="40,740" zPosition="-2" size="1840,340" backgroundColor="background" transparent="0" />
  	<widget name="Video_size" font="Prive4;27" position="50,766" size="210,31" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />

    <widget source="session.CurrentService" render="Label" position="265,754" size="877,48" font="Prive4;38" noWrap="1" halign="left" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2" valign="bottom">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="987,766" size="660,30" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1659,754" size="135,48" font="Prive4;39" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1775,757" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <eLabel position="70,818" zPosition="8" size="1780,1" backgroundColor="#1546AF" transparent="0" />
    <ePixmap position="61,819" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="80,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />   
  
    <widget name="Prov_temp_rpm" position="1226,826" size="625,33" font="Prive3;27" halign="right" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />
    
    <widget position="265,828" size="90,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <eLabel text="- " font="Prive4;27" position="355,828" size="10,39" halign="left" valign="bottom" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background"/>
    <widget position="371,828" size="90,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">EndTime</convert>
    </widget>
    <widget position="467,828" size="689,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1159,828" size="142,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" halign="right" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" backgroundColor="#1546AF" position="265,882" size="1036,5" zPosition="3" transparent="0">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="265,877" size="0,0" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />    
    <widget position="265,892" size="90,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <eLabel text="- " font="Prive4;27" position="355,892" size="10,39" halign="left" valign="bottom" foregroundColor="un99bad6" transparent="1" backgroundColor="background"/>
    <widget position="371,892" size="90,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">EndTime</convert>
    </widget>
    <widget position="467,892" size="689,39" source="session.Event_Next" render="g17EmptyEpg" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6" transparent="1" backgroundColor="background">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1159,892" size="142,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" halign="right" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1809,871" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1809,871" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1809,871" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1809,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1809,871" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1809,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1809,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1809,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1809,871" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1809,871" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1809,871" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    <eLabel position="70,942" zPosition="8" size="1780,1" backgroundColor="#1546AF" transparent="0" />    
    <widget name="TP_type" position="71,952" zPosition="2" size="293,30" font="Prive4;22" halign="left" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget name="TP_info" position="265,951" zPosition="1" size="735,30" font="Prive4;24" halign="center" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />

    <widget name="Dtype" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
          	
    <eLabel text="Snr:" font="Prive4;20" position="71,1008" size="60,30" halign="left" foregroundColor="un99bad6" transparent="1" backgroundColor="background"/>
    <widget source="session.FrontendStatus" render="Label" position="135,1008" size="105,30" font="Prive4;20" halign="left" zPosition="5" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17ExtraSource">SnrdB2</convert>
    </widget>
    <ePixmap pixmap="hd_glass17/slider/sigsnrbar_back43.png" position="71,993" size="230,6" zPosition="1" alphatest="on"/>
  	<widget source="session.FrontendStatus" render="Progress" position="71,993" size="230,6" zPosition="2" pixmap="hd_glass17/slider/sigbar43.png" transparent="1" >
    <convert type="g17ExtraSource">SnrNum</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" position="196,1008" size="105,30" font="Prive4;20" halign="right" zPosition="5" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendInfo" render="g17TunersLabel" font="Regular2;20" PosLR="left" position="685,1012" alphatest="off" size="247,30" zPosition="5" tuners="5" ActiveTunerColor="#0000d100" backgroundColor="background" BackgroundActiveTunerColor="#00ecb100"/>

    <widget name="bitrate_info" position="325,1008" zPosition="4" size="400,30" font="Prive4;20" halign="left" backgroundColor="background" transparent="1"/>    
    <widget name="ecmLineInfo" position="589,1009" size="1258,24" font="Prive4;18" noWrap="1" halign="right" backgroundColor="background" foregroundColor="unb2e0b4" zPosition="6" transparent="1" />

		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>	
    <widget name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    </screen>"""

g17_extraScreen["63"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <ePixmap position="0,0" zPosition="-2" size="1920,1080" pixmap="hd_glass17/general/infobar-ex63.png" alphatest="off" />
  	<widget name="Video_size" font="Prive4;28" position="100,766" size="217,33" halign="center" backgroundColor="lightblue" transparent="1" />

    <widget position="315,757" size="757,48" source="session.CurrentService" render="Label" font="Prive4;37" valign="bottom" halign="left" noWrap="1" backgroundColor="black" foregroundColor="red" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="937,762" size="660,30" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1609,757" size="135,48" font="Prive4;36" valign="top" halign="right" backgroundColor="black" foregroundColor="red" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1725,760" size="69,34" font="Prive4;30" valign="top" halign="right" backgroundColor="black" foregroundColor="blue" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <ePixmap position="111,819" size="189,123" pixmap="hd_glass17/frame_hd.png" backgroundColor="black" zPosition="1" alphatest="blend" />
    <widget name="g17picon" position="130,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />   
  
    <widget name="Prov_temp_rpm" position="1027,832" size="607,37" font="Prive4;27" halign="right" transparent="1" backgroundColor="black" foregroundColor="un99bad6" />

    <ePixmap position="1635,819" size="189,123" pixmap="hd_glass17/frame_hd.png" backgroundColor="black" zPosition="1" alphatest="blend" />
    <widget name="picProvSat" position="1654,835" size="150,90" zPosition="2" transparent="1" alphatest="on" />    
    <widget name="weaTxt" position="1654,835" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
    
    <widget position="315,828" size="112,39" source="session.Event_Now" render="Label" zPosition="1" transparent="1" backgroundColor="black" font="Prive4;31" valign="bottom" foregroundColor="green">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="426,828" size="495,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="black" zPosition="-1" font="Prive4;31" valign="bottom" noWrap="1" foregroundColor="yellow">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,828" size="150,39" source="session.Event_Now" render="Label" transparent="1" backgroundColor="black" zPosition="1" font="Prive4;31" valign="bottom" foregroundColor="green" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="313,874" size="762,21" zPosition="3" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="313,874" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />    
    <widget position="315,892" size="112,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="black" font="Prive4;31" valign="bottom" foregroundColor="yellow">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="426,892" size="495,39" source="session.Event_Next" render="g17EmptyEpg" transparent="1" backgroundColor="black" font="Prive4;31" valign="bottom" noWrap="1" foregroundColor="green">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="909,892" size="150,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="black" font="Prive4;31" valign="bottom" foregroundColor="yellow" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1597,871" size="72,72" backgroundColor="black" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="blend" />
    <widget name="wide" position="1597,871" size="72,72" backgroundColor="black" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="blend" />
    <widget name="dolby" position="1597,871" size="72,72" backgroundColor="black" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="blend" />
    <widget name="multi_audio" position="1597,871" size="72,72" backgroundColor="black" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="blend" />
    <widget name="txt" position="1597,871" size="72,72" backgroundColor="black" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="blend" />
    <widget name="hd_sd" position="1569,871" size="72,72" backgroundColor="black" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="blend" />
    <widget name="hbb" position="1569,871" size="72,72" backgroundColor="black" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="blend" />
    <widget name="subtit" position="1569,871" size="72,72" backgroundColor="black" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="blend" />
    <widget name="tuner" position="1597,871" size="42,72" zPosition="1" backgroundColor="black" alphatest="blend" />
    <widget name="HDD_state" position="1597,871" size="42,72" zPosition="1" backgroundColor="black" alphatest="blend" />    
    <widget position="1597,871" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" backgroundColor="black" zPosition="2" alphatest="blend">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
        
    <ePixmap position="120,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <ePixmap position="960,942" zPosition="8" size="840,1" pixmap="hd_glass17/tib.png" />
    <widget name="TP_type" position="121,952" zPosition="2" size="293,30" font="Prive4;22" halign="left" transparent="1" backgroundColor="black" foregroundColor="un99bad6" />
    <widget name="TP_info" position="315,951" zPosition="1" size="735,30" font="Prive4;24" halign="center" transparent="1" backgroundColor="black" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1734,951" size="78,46" zPosition="3" backgroundColor="black" alphatest="blend" />
    <widget name="Dcam" position="1734,951" size="78,46" zPosition="3" backgroundColor="black" alphatest="blend" />
    <widget name="Decm" position="1734,951" size="78,46" zPosition="3" backgroundColor="black" alphatest="blend" />
    <widget name="Dnetstate" position="1723,951" size="78,46" zPosition="3" backgroundColor="black" alphatest="blend" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1734,951" size="78,46" backgroundColor="black" zPosition="3" alphatest="blend" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1734,951" size="78,46" backgroundColor="black" zPosition="3" alphatest="blend" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1734,951" size="78,46" backgroundColor="black" zPosition="3" alphatest="blend" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1734,951" size="78,46" backgroundColor="black" zPosition="3" alphatest="blend" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1734,951" size="78,46" backgroundColor="black" zPosition="3" alphatest="blend" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1734,944" size="78,46" backgroundColor="black" zPosition="3" alphatest="blend" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1734,951" size="78,46" backgroundColor="black" zPosition="3" alphatest="blend" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1734,951" size="78,46" backgroundColor="black" zPosition="3" alphatest="blend" />
      	
  	<widget source="session.FrontendStatus" render="Progress" position="345,1005" size="300,7" zPosition="2" pixmap="hd_glass17/slider/sigbar.png" transparent="1" >
    <convert type="g17ExtraSource">SnrNum</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Progress" position="825,1005" size="300,7" zPosition="2" pixmap="hd_glass17/slider/sigbar.png" transparent="1" >
    <convert type="g17ExtraSource">AgcNum</convert>
    </widget>

    <ePixmap pixmap="hd_glass17/slider/sigsnrbar_back.png" position="345,1005" size="300,7" zPosition="1" alphatest="on"/>
    <ePixmap pixmap="hd_glass17/slider/sigbar_back.png" position="825,1005" size="300,7" zPosition="1" alphatest="on"/>

    <eLabel text="Snr: dB" font="Prive4;27" position="121,988" size="125,30" foregroundColor="green" backgroundColor="black" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="241,988" size="100,30" font="Prive4;27" transparent="1" backgroundColor="black" zPosition="5" foregroundColor="white">
      <convert type="g17ExtraSource">SnrdB</convert>
    </widget>
  
    <widget source="session.FrontendStatus" render="Label" position="660,988" size="75,33" transparent="1" font="Prive4;27" zPosition="1" backgroundColor="black" foregroundColor="white">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="757,988" size="60,30" font="Prive4;27" foregroundColor="yellow" transparent="1" backgroundColor="black" />
    <widget source="session.FrontendStatus" render="Label" position="1140,988" size="75,30" transparent="1" font="Prive4;27" backgroundColor="black" foregroundColor="white">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    
    <widget name="bitrate_info" position="1377,991" zPosition="8" size="750,30" font="Prive3;27" halign="left" backgroundColor="black" foregroundColor="red" transparent="1"/>
		<widget name="ecmlabels" font="Prive3;24" position="100,225" zPosition="2" size="150,361" backgroundColor="black" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="183,225" zPosition="3" size="318,361" backgroundColor="black" transparent="1" />
    <widget name="back_enhanced" position="52,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-63.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="112,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="310,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="112,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="310,572"  size="150,90"  zPosition="2" alphatest="on"/> 
    <widget  name="caidPids" transparent="1" position="529,157" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="black" />
    <widget name="caidPids_back" position="499,97"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-63.png" alphatest="off" zPosition="-1" />  	 	
    <widget name="active_caidPid" transparent="1" position="529,157" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="black" />
    <widget name="caidPids_end" position="499,163"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-63.png" alphatest="off" zPosition="3" />

	</screen>"""

g17_extraScreen["64"] = """
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""
g17_extraScreen["64"]  += '<ePixmap position="75,585" zPosition="-2" size="1770,465" pixmap="'+PATH+'/64/infobar-47.png" alphatest="off" />\n'
g17_extraScreen["64"]  += '<widget  name="back_enhanced" alphatest="off" position="52,55" size="465,601" pixmap="'+PATH+'/64/back_enhanced-51.png" zPosition="0" />\n'
g17_extraScreen["64"]  += '<widget name="caidPids_back" alphatest="off" position="1609,15" size="255,600" pixmap="'+PATH+'/64/back_caidPids-44.png" zPosition="0" />\n'
g17_extraScreen["64"]  += '<widget name="caidPids_end" alphatest="off" position="1609,85" size="255,9" pixmap="'+PATH+'/64/end_caidPids-44.png" zPosition="3" />\n'
g17_extraScreen["64"]  += """

<widget position="703,594" size="843,67" source="session.CurrentService" render="Label" font="Prive4;45" zPosition="2" valign="center" halign="left" noWrap="1" backgroundColor="#31000000" foregroundColor="white" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
		
    <widget source="session.FrontendStatus" render="Progress" position="1635,774" size="7,112" zPosition="4" pixmap="hd_glass17/icons/bar.png" orientation="orBottomToTop" transparent="1" >
    <convert type="g17ExtraSource">SnrNum</convert>                          
    </widget>
    <widget source="session.FrontendStatus" render="Progress" position="1807,774" size="7,112" zPosition="4" pixmap="hd_glass17/icons/bar.png" orientation="orBottomToTop" transparent="1" >
    <convert type="g17ExtraSource">AgcNum</convert>
    </widget>

    <ePixmap pixmap="hd_glass17/icons/bar_back.png" position="1635,774" size="7,112" zPosition="1" alphatest="on"/>
    <ePixmap pixmap="hd_glass17/icons/bar_back.png" position="1807,774" size="7,112" zPosition="1" alphatest="on"/>

    <eLabel text="Snr:" font="Prive3;25" position="1662,774" zPosition="2" size="142,30" halign="left" backgroundColor="#31000000" foregroundColor="#999999" transparent="1" />
    <eLabel text="Agc:" font="Prive3;25" position="1662,816" zPosition="2" size="142,30" halign="left" backgroundColor="#31000000" foregroundColor="#999999" transparent="1" />
    <eLabel text="Ber:" font="Prive3;25" position="1662,858" zPosition="4" size="142,30" halign="left" backgroundColor="#31000000" foregroundColor="#999999" transparent="1" />

    <widget source="session.FrontendStatus" render="Label" font="Prive3;25" position="1722,774" zPosition="5" backgroundColor="#31000000" size="105,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;25" position="1722,816" zPosition="5" backgroundColor="#31000000" size="105,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;25" position="1722,858" zPosition="5" backgroundColor="#31000000" size="105,30" halign="left" transparent="1"  >
    <convert type="FrontendInfo">BER</convert> 
    </widget>    		
    
    <widget name="TP_info" position="390,1006" zPosition="1" size="1200,45" font="Prive4;30"  valign="center" halign="left" noWrap="1" backgroundColor="#31000000" foregroundColor="white" transparent="1" />
    <widget name="TP_type" position="90,1006" zPosition="1" size="300,45" font="Prive4;30"  valign="center" halign="left" noWrap="1" backgroundColor="#31000000" foregroundColor="white" transparent="1" />
    <widget name="bitrate_info" position="1290,945" zPosition="1" size="0,0" font="Prive4;31" noWrap="1" valign="center" halign="right" backgroundColor="#31000000" foregroundColor="white" transparent="1" />
    <widget name="ecmLineInfo" position="90,945" size="1500,43" font="Prive4;25" noWrap="1" valign="center" halign="left" backgroundColor="#31000000" transparent="1" foregroundColor="unb2e0b4" zPosition="5" />

    <widget name="Video_size" font="Prive4;31" position="1605,945" size="210,43" valign="center" halign="right" noWrap="1" backgroundColor="#31000000" foregroundColor="white" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1527,697" size="225,45" font="Prive4;37"  valign="top" halign="right" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format:%H:%M</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1752,699" size="75,45" font="Prive4;31"  valign="top" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A, %d.%B %Y" position="1153,601" size="660,45" font="Prive3;27" halign="right" valign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    
    <widget name="Prov_temp_rpm" position="90,1006" size="0,0" font="Prive4;30" halign="left" backgroundColor="#31000000" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />

    <widget name="g17picon" position="75,675" size="600,255" zPosition="2" transparent="1" alphatest="on" />
    <widget source="session.CurrentService" render="g17PicRef" position="690,675" size="150,90" zPosition="2" transparent="1" alphatest="on">
      <convert type="ServiceName">Reference</convert>
    </widget>    
    <widget position="703,787" size="202,45" source="session.Event_Now" backgroundColor="#31000000" transparent="1" valign="center" render="Label" zPosition="1" font="Prive4;37" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="835,787" size="754,45" source="session.Event_Now" backgroundColor="#31000000" transparent="1" valign="center" render="g17EmptyEpg" zPosition="2" font="Prive4;39"  noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1465,832" size="130,45" source="session.Event_Now" backgroundColor="#31000000" transparent="1" render="Label" zPosition="1" font="Prive3;27" valign="center" foregroundColor="unb2e0b4" halign="center">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="703,847" size="762,21" zPosition="6" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="703,847" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="5" alphatest="on" />
 
    <widget position="703,877" size="202,45" source="session.Event_Next" backgroundColor="#31000000" transparent="1" valign="center" render="Label" font="Prive4;37"  zPosition="5" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="835,877" size="754,45" source="session.Event_Next" backgroundColor="#31000000" transparent="1" valign="center" render="g17EmptyEpg" font="Prive4;39"  zPosition="6" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>

    <widget name="subserv" position="1543,691" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1543,691" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1543,691" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1543,691" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1543,691" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1543,691" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1543,691" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1543,691" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1543,691" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
        
		<widget name="ecmlabels" font="Prive3;24" position="100,190" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="183,190" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="picProv" position="112,79" size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="310,79" size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="112,539" size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="310,539" size="150,90"  zPosition="2" alphatest="on"/>

    <widget  name="caidPids" transparent="1" position="1639,75" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="active_caidPid" transparent="1" position="1639,75" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    
  </screen>"""

g17_extraScreen["65"] = """
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">"""
g17_extraScreen["65"]  += '<ePixmap position="75,585" zPosition="-2" size="1770,465" pixmap="'+PATH+'/65/infobar-47.png" alphatest="off" />\n'
g17_extraScreen["65"]  += '<widget  name="back_enhanced" alphatest="off" position="52,55" size="465,601" pixmap="'+PATH+'/65/back_enhanced-51.png" zPosition="0" />\n'
g17_extraScreen["65"]  += '<widget name="caidPids_back" alphatest="off" position="1609,15" size="255,600" pixmap="'+PATH+'/65/back_caidPids-44.png" zPosition="0" />\n'
g17_extraScreen["65"]  += '<widget name="caidPids_end" alphatest="off" position="1609,85" size="255,9" pixmap="'+PATH+'/65/end_caidPids-44.png" zPosition="3" />\n'
g17_extraScreen["65"]  += """

<widget position="703,594" size="843,67" source="session.CurrentService" render="Label" font="Prive4;45" zPosition="2" valign="center" halign="left" noWrap="1" backgroundColor="#31000000" foregroundColor="white" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
		
    <widget source="session.FrontendStatus" render="Progress" position="1635,774" size="7,112" zPosition="4" pixmap="hd_glass17/icons/bar.png" orientation="orBottomToTop" transparent="1" >
    <convert type="g17ExtraSource">SnrNum</convert>                          
    </widget>
    <widget source="session.FrontendStatus" render="Progress" position="1807,774" size="7,112" zPosition="4" pixmap="hd_glass17/icons/bar.png" orientation="orBottomToTop" transparent="1" >
    <convert type="g17ExtraSource">AgcNum</convert>
    </widget>

    <ePixmap pixmap="hd_glass17/icons/bar_back.png" position="1635,774" size="7,112" zPosition="1" alphatest="on"/>
    <ePixmap pixmap="hd_glass17/icons/bar_back.png" position="1807,774" size="7,112" zPosition="1" alphatest="on"/>

    <eLabel text="Snr:" font="Prive3;25" position="1662,774" zPosition="2" size="142,30" halign="left" backgroundColor="#31000000" foregroundColor="#999999" transparent="1" />
    <eLabel text="Agc:" font="Prive3;25" position="1662,816" zPosition="2" size="142,30" halign="left" backgroundColor="#31000000" foregroundColor="#999999" transparent="1" />
    <eLabel text="Ber:" font="Prive3;25" position="1662,858" zPosition="4" size="142,30" halign="left" backgroundColor="#31000000" foregroundColor="#999999" transparent="1" />

    <widget source="session.FrontendStatus" render="Label" font="Prive3;25" position="1722,774" zPosition="5" backgroundColor="#31000000" size="105,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;25" position="1722,816" zPosition="5" backgroundColor="#31000000" size="105,30" halign="left" transparent="1" >
    <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" font="Prive3;25" position="1722,858" zPosition="5" backgroundColor="#31000000" size="105,30" halign="left" transparent="1"  >
    <convert type="FrontendInfo">BER</convert> 
    </widget>    		
    
    <widget name="TP_info" position="390,1006" zPosition="1" size="1200,45" font="Prive4;30"  valign="center" halign="left" noWrap="1" backgroundColor="#31000000" foregroundColor="white" transparent="1" />
    <widget name="TP_type" position="90,1006" zPosition="1" size="300,45" font="Prive4;30"  valign="center" halign="left" noWrap="1" backgroundColor="#31000000" foregroundColor="white" transparent="1" />
    <widget name="bitrate_info" position="1225,945" zPosition="1" size="600,45" font="Prive4;25" noWrap="1" valign="center" halign="right" backgroundColor="#31000000" foregroundColor="white" transparent="1" />
    <widget name="ecmLineInfo" position="90,945" size="1500,43" font="Prive4;25" noWrap="1" valign="center" halign="left" backgroundColor="#31000000" transparent="1" foregroundColor="unb2e0b4" zPosition="5" />

    <widget name="Video_size" font="Prive3;25" position="1635,892" size="190,30" valign="center" halign="center" noWrap="1" backgroundColor="#31000000" foregroundColor="white" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1527,697" size="225,45" font="Prive4;37"  valign="top" halign="right" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format:%H:%M</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1752,699" size="75,45" font="Prive4;31"  valign="top" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A, %d.%B %Y" position="1153,601" size="660,45" font="Prive3;27" halign="right" valign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    
    <widget name="Prov_temp_rpm" position="90,1006" size="0,0" font="Prive4;30" halign="left" backgroundColor="#31000000" foregroundColor="un99bad6" />

    <widget name="Dtype" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1759,1003" size="78,46" zPosition="3" alphatest="off" />

    <widget name="g17picon" position="75,675" size="600,255" zPosition="2" transparent="1" alphatest="on" />
    <widget source="session.CurrentService" render="g17PicRef" position="690,675" size="150,90" zPosition="2" transparent="1" alphatest="on">
      <convert type="ServiceName">Reference</convert>
    </widget>    
    <widget position="703,787" size="202,45" source="session.Event_Now" backgroundColor="#31000000" transparent="1" valign="center" render="Label" zPosition="1" font="Prive4;37" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="835,787" size="754,45" source="session.Event_Now" backgroundColor="#31000000" transparent="1" valign="center" render="g17EmptyEpg" zPosition="2" font="Prive4;39"  noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1465,832" size="130,45" source="session.Event_Now" backgroundColor="#31000000" transparent="1" render="Label" zPosition="1" font="Prive3;27" valign="center" foregroundColor="unb2e0b4" halign="center">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="703,847" size="762,21" zPosition="6" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="703,847" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="5" alphatest="on" />
 
    <widget position="703,877" size="202,45" source="session.Event_Next" backgroundColor="#31000000" transparent="1" valign="center" render="Label" font="Prive4;37"  zPosition="5" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="835,877" size="754,45" source="session.Event_Next" backgroundColor="#31000000" transparent="1" valign="center" render="g17EmptyEpg" font="Prive4;39"  zPosition="6" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>

    <widget name="subserv" position="1543,691" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1543,691" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1543,691" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1543,691" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1543,691" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1543,691" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1543,691" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1543,691" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1543,691" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
        
		<widget name="ecmlabels" font="Prive3;24" position="100,190" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="183,190" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="picProv" position="112,79" size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="310,79" size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="112,539" size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="310,539" size="150,90"  zPosition="2" alphatest="on"/>

    <widget  name="caidPids" transparent="1" position="1639,75" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="active_caidPid" transparent="1" position="1639,75" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    
  </screen>"""

g17_extraScreen["70"] = """
                                             
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
<ePixmap position="0,826" zPosition="-2" size="1920,495" pixmap="hd_glass17/general/infobar-57.png" alphatest="off" />

	  <widget source="session.CurrentService" render="Label" position="320,870" size="1000,52" font="Prive4;38" halign="left" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">	
    <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>

    <eLabel position="70,1010" zPosition="8" size="1780,2" backgroundColor="#1546AF" transparent="0" />

    <widget name="TP_type" position="323,1017" zPosition="1" size="293,30" font="Prive4;22" halign="left" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />
    <widget name="TP_info" position="870,1017" zPosition="2" size="851,30" font="Prive4;22" halign="left" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

    <widget name="Video_size" font="Prive4;22" position="74,1017" size="220,33" halign="center" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />
    <widget name="Prov_temp_rpm" font="Prive4;22" position="1217,1017" size="630,37" halign="right" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

    <widget source="global.CurrentTime" render="Label" position="1659,870" size="135,48" font="Prive4;38" valign="top" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1775,872" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="996,883" size="660,33" font="Prive3;27" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1" />
    
    <widget name="g17picon" position="74,871" size="220,132" zPosition="2" transparent="1" alphatest="blend" />

    <widget position="322,932" size="90,39" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="418,932" size="595,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1038,932" size="142,39" source="session.Event_Now" render="Label" zPosition="1" backgroundColor="background" transparent="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" backgroundColor="#1546AF" position="325,927" size="853,4" zPosition="3" transparent="0">
      <convert type="EventTime">Progress</convert>
    </widget>
 <widget name="slider_back" position="320,913" size="0,0" pixmap="hd_glass17/slider/slider_back57.png" zPosition="2" alphatest="blend" />
    <widget position="322,965" size="90,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="418,965" size="595,39" source="session.Event_Next" render="g17EmptyEpg" backgroundColor="background" transparent="1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1038,965" size="142,39" source="session.Event_Next" render="Label" backgroundColor="background" transparent="1" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    <widget name="Dtype" position="1773,987" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1773,987" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1773,987" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1773,987" size="0,0" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1773,987" size="0,0" zPosition="3" alphatest="off" />
    
    <widget name="subserv" position="1810,927" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1810,927" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1810,927" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1810,927" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1810,927" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1810,927" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1810,927" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1810,927" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1810,927" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1810,927" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1810,927" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget> 
    <widget name="ecmLineInfo" position="589,1009" size="0,0" font="Prive4;18" noWrap="1" halign="right" backgroundColor="background" foregroundColor="unb2e0b4" zPosition="5" transparent="1" />
    
    <eLabel text="Snr:dB" font="Prive4;22" position="503,1017" size="105,30" foregroundColor="un99bad6" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="586,1017" size="90,30" font="Prive4;22" transparent="1" backgroundColor="background" zPosition="5" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">SnrdB</convert>
    </widget>
    <eLabel text="-" position="643,1017" size="60,30" font="Prive4;22" foregroundColor="un99bad6" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="660,1017" size="90,30" transparent="1" backgroundColor="background" font="Prive4;22" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="737,1017" size="60,30" font="Prive4;22" foregroundColor="un99bad6" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="792,1017" size="90,30" transparent="1" backgroundColor="background" font="Prive4;22" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="caidPids" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" transparent="1" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    
  </screen>"""
	
g17_extraScreen["71"] = """
                                             
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
<ePixmap position="0,826" zPosition="-2" size="1920,495" pixmap="hd_glass17/general/infobar-57.png" alphatest="off" />

	  <widget source="session.CurrentService" render="Label" position="320,870" size="1000,52" font="Prive4;38" halign="left" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">	
    <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>

    <eLabel position="70,1010" zPosition="8" size="1780,2" backgroundColor="#1546AF" transparent="0" />

    <widget name="TP_type" position="323,1017" zPosition="1" size="293,30" font="Prive4;22" halign="left" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />
    <widget name="TP_info" position="737,1017" zPosition="2" size="951,30" font="Prive4;22" halign="left" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

    <widget name="Video_size" font="Prive4;22" position="74,1017" size="220,33" halign="center" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />
    <widget name="Prov_temp_rpm" font="Prive4;22" position="1217,1017" size="630,37" halign="right" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

    <widget source="global.CurrentTime" render="Label" position="1659,870" size="135,48" font="Prive4;38" valign="top" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1775,872" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="996,883" size="660,33" font="Prive3;27" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1" />
    
    <widget name="g17picon" position="74,871" size="220,132" zPosition="2" transparent="1" alphatest="blend" />

    <widget position="322,932" size="90,39" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="418,932" size="595,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1038,932" size="142,39" source="session.Event_Now" render="Label" zPosition="1" backgroundColor="background" transparent="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" backgroundColor="#1546AF" position="325,927" size="853,4" zPosition="3" transparent="0">
      <convert type="EventTime">Progress</convert>
    </widget>
 <widget name="slider_back" position="320,913" size="0,0" pixmap="hd_glass17/slider/slider_back57.png" zPosition="2" alphatest="blend" />
    <widget position="322,965" size="90,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="418,965" size="595,39" source="session.Event_Next" render="g17EmptyEpg" backgroundColor="background" transparent="1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1038,965" size="142,39" source="session.Event_Next" render="Label" backgroundColor="background" transparent="1" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    <widget name="Dtype" position="1773,987" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1773,987" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1773,987" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1773,987" size="0,0" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1773,987" size="0,0" zPosition="3" alphatest="off" />
    
    <widget name="subserv" position="1810,927" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1810,927" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1810,927" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1810,927" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1810,927" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1810,927" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1810,927" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1810,927" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1810,927" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1810,927" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1810,927" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget> 
    <widget name="ecmLineInfo" position="589,1009" size="0,0" font="Prive4;18" noWrap="1" halign="right" backgroundColor="background" foregroundColor="unb2e0b4" zPosition="5" transparent="1" />
    
    <eLabel text="Snr:dB" font="Prive4;22" position="503,1017" size="105,30" foregroundColor="un99bad6" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="586,1017" size="90,30" font="Prive4;22" transparent="1" backgroundColor="background" zPosition="5" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">SnrdB</convert>
    </widget>
    <eLabel text="-" position="643,1017" size="60,30" font="Prive4;22" foregroundColor="un99bad6" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="660,1017" size="90,30" transparent="1" backgroundColor="background" font="Prive4;22" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="caidPids" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" transparent="1" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    
  </screen>"""

g17_extraScreen["72"] = """

  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
<ePixmap position="0,796" zPosition="-2" size="1920,495" pixmap="hd_glass17/general/infobar-57.png" alphatest="off" />

	  <widget source="session.CurrentService" render="Label" position="320,840" size="1000,52" font="Prive4;38" halign="left" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">	
    <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>

    <eLabel position="70,980" zPosition="8" size="1780,2" backgroundColor="#1546AF" transparent="0" />
    <eLabel position="70,1018" zPosition="8" size="1780,2" backgroundColor="#1546AF" transparent="0" />

    <widget name="TP_type" position="323,985" zPosition="1" size="293,30" font="Prive4;22" halign="left" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />
    <widget name="TP_info" position="870,985" zPosition="2" size="851,30" font="Prive4;22" halign="left" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

    <widget name="Video_size" font="Prive4;22" position="74,985" size="220,33" halign="center" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />
    <widget name="Prov_temp_rpm" font="Prive4;22" position="1215,985" size="630,37" halign="right" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

    <widget source="global.CurrentTime" render="Label" position="1659,840" size="135,48" font="Prive4;38" valign="top" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1775,842" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="996,853" size="660,33" font="Prive3;27" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1" />
    
    <widget name="g17picon" position="74,841" size="220,132" zPosition="2" transparent="1" alphatest="blend" />

    <widget position="322,902" size="90,39" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="418,902" size="595,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1038,902" size="142,39" source="session.Event_Now" render="Label" zPosition="1" backgroundColor="background" transparent="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" backgroundColor="#1546AF" position="325,897" size="853,4" zPosition="3" transparent="0">
      <convert type="EventTime">Progress</convert>
    </widget>

    <widget position="322,935" size="90,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="418,935" size="595,39" source="session.Event_Next" render="g17EmptyEpg" backgroundColor="background" transparent="1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1038,935" size="142,39" source="session.Event_Next" render="Label" backgroundColor="background" transparent="1" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    <widget name="Dtype" position="1773,957" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1773,957" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1773,967" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1773,967" size="0,0" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1773,967" size="0,0" zPosition="3" alphatest="off" />
    
    <widget name="subserv" position="1810,897" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1810,897" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1810,897" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1810,897" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1810,897" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1810,897" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1810,897" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1810,897" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1810,897" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1810,897" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1810,897" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget> 
    <widget name="ecmLineInfo" position="70,1025" size="1780,24" font="Prive4;16" noWrap="1" halign="center" transparent="1" backgroundColor="background" foregroundColor="un99bad6" zPosition="5" />
    
    <eLabel text="Snr:dB" font="Prive4;22" position="503,985" size="105,30" foregroundColor="un99bad6" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="586,985" size="90,30" font="Prive4;22" transparent="1" backgroundColor="background" zPosition="5" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">SnrdB</convert>
    </widget>
    <eLabel text="-" position="643,985" size="60,30" font="Prive4;22" foregroundColor="un99bad6" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="660,985" size="90,30" transparent="1" backgroundColor="background" font="Prive4;22" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="737,985" size="60,30" font="Prive4;22" foregroundColor="un99bad6" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="792,985" size="90,30" transparent="1" backgroundColor="background" font="Prive4;22" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="caidPids" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" transparent="1" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />    
  </screen>"""

g17_extraScreen["73"] = """
                                             
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
<ePixmap position="0,796" zPosition="-2" size="1920,495" pixmap="hd_glass17/general/infobar-57.png" alphatest="off" />

	  <widget source="session.CurrentService" render="Label" position="320,840" size="1000,52" font="Prive4;38" halign="left" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">	
    <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>

    <eLabel position="70,980" zPosition="8" size="1780,2" backgroundColor="#1546AF" transparent="0" />
    <eLabel position="70,1018" zPosition="8" size="1780,2" backgroundColor="#1546AF" transparent="0" />

    <widget name="TP_type" position="323,985" zPosition="1" size="293,30" font="Prive4;22" halign="left" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />
    <widget name="TP_info" position="737,985" zPosition="2" size="851,30" font="Prive4;22" halign="left" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

    <widget name="Video_size" font="Prive4;22" position="74,985" size="220,33" halign="center" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />
    <widget name="Prov_temp_rpm" font="Prive4;22" position="1215,985" size="630,37" halign="right" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

    <widget source="global.CurrentTime" render="Label" position="1659,840" size="135,48" font="Prive4;38" valign="top" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1775,842" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="996,853" size="660,33" font="Prive3;27" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1" />
    
    <widget name="g17picon" position="74,841" size="220,132" zPosition="2" transparent="1" alphatest="blend" />

    <widget position="322,902" size="90,39" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="418,902" size="595,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1038,902" size="142,39" source="session.Event_Now" render="Label" zPosition="1" backgroundColor="background" transparent="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" backgroundColor="#1546AF" position="325,897" size="853,4" zPosition="3" transparent="0">
      <convert type="EventTime">Progress</convert>
    </widget>

    <widget position="322,935" size="90,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;27" valign="bottom" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="418,935" size="595,39" source="session.Event_Next" render="g17EmptyEpg" backgroundColor="background" transparent="1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1038,935" size="142,39" source="session.Event_Next" render="Label" backgroundColor="background" transparent="1" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    <widget name="Dtype" position="1773,957" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1773,957" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1773,967" size="0,0" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1773,967" size="0,0" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1773,967" size="0,0" zPosition="3" alphatest="off" />
    
    <widget name="subserv" position="1810,897" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1810,897" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1810,897" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1810,897" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1810,897" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1810,897" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1810,897" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1810,897" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1810,897" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1810,897" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1810,897" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget> 
    <widget name="ecmLineInfo" position="70,1025" size="1780,24" font="Prive4;16" noWrap="1" halign="right" transparent="1" backgroundColor="background" foregroundColor="un99bad6" zPosition="5" />
    <widget name="bitrate_info" position="70,1025" zPosition="6" size="1000,24" font="Prive4;16" noWrap="1" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="5" />
    
    <eLabel text="Snr:dB" font="Prive4;22" position="503,985" size="105,30" foregroundColor="un99bad6" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="586,985" size="90,30" font="Prive4;22" transparent="1" backgroundColor="background" zPosition="5" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">SnrdB</convert>
    </widget>
    <eLabel text="-" position="643,985" size="60,30" font="Prive4;22" foregroundColor="un99bad6" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="660,985" size="90,30" transparent="1" backgroundColor="background" font="Prive4;22" foregroundColor="unb2e0b4">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="caidPids" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" transparent="1" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />    
  </screen>"""

g17_extraScreen["74"] = """
                                             
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
<ePixmap position="0,818" zPosition="-2" size="1920,495" pixmap="hd_glass17/general/infobar-57.png" alphatest="off" />

	  <widget source="session.CurrentService" render="Label" position="326,858" size="1000,52" font="Prive4;36" halign="left" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">	
    <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>

    <eLabel position="325,981" zPosition="8" size="1525,2" backgroundColor="#1546AF" transparent="0" />
    <eLabel position="70,1018" zPosition="8" size="228,2" backgroundColor="#1546AF" transparent="0" />
    <eLabel position="325,1018" zPosition="8" size="1525,2" backgroundColor="#1546AF" transparent="0" />

    <widget name="TP_type" position="327,987" zPosition="1" size="293,30" font="Prive4;20" halign="left" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />
    <widget name="TP_info" position="870,987" zPosition="2" size="851,30" font="Prive4;20" halign="left" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

    <widget name="Video_size" font="Prive4;18" position="74,1024" size="220,33" halign="center" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />
    <widget name="Prov_temp_rpm" font="Prive4;20" position="1217,987" size="630,37" halign="right" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

    <widget source="global.CurrentTime" render="Label" position="1659,858" size="135,48" font="Prive4;36" valign="top" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1775,861" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="996,869" size="660,33" font="Prive3;27" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1" />
    
    <widget name="g17picon" position="74,871" size="220,132" zPosition="2" transparent="1" alphatest="blend" />

    <widget position="326,908" size="90,39" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" zPosition="1" font="Prive4;24" valign="bottom" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="418,908" size="750,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="-1" font="Prive4;24" valign="bottom" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1138,908" size="142,39" source="session.Event_Now" render="Label" zPosition="1" backgroundColor="background" transparent="1" font="Prive4;24" valign="bottom" foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" backgroundColor="#1546AF" position="325,908" size="957,4" zPosition="3" transparent="0">
      <convert type="EventTime">Progress</convert>
    </widget>

    <widget position="326,937" size="90,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;24" valign="bottom" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="418,937" size="750,39" source="session.Event_Next" render="g17EmptyEpg" backgroundColor="background" transparent="1" font="Prive4;24" valign="bottom" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1138,937" size="142,39" source="session.Event_Next" render="Label" backgroundColor="background" transparent="1" font="Prive4;24" valign="bottom" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    <widget name="Dtype" position="1773,957" size="39,27" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1773,957" size="39,27" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1773,967" size="39,27" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1773,967" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1809,1025" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="702,892" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="702,892" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="702,892" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="702,892" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="702,892" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="702,892" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="702,892" size="39,27" zPosition="3" alphatest="off" />
    
    <widget name="subserv" position="1810,908" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1810,908" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1810,908" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1810,908" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1810,908" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1810,908" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1810,908" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1810,908" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1810,908" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1810,908" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1810,908" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget> 
    <widget name="ecmLineInfo" position="328,1024" size="1300,30" font="Prive4;18" noWrap="1" halign="left" transparent="1" backgroundColor="background" foregroundColor="un99bad6" zPosition="5" />
    
    <eLabel text="Snr:dB" font="Prive4;20" position="503,987" size="105,30" foregroundColor="#6cbcf0" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="586,987" size="90,30" font="Prive4;20" transparent="1" backgroundColor="background" zPosition="5" foregroundColor="#6cbcf0">
      <convert type="g17ExtraSource">SnrdB</convert>
    </widget>
    <eLabel text="-" position="643,987" size="60,30" font="Prive4;20" foregroundColor="#6cbcf0" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="660,987" size="90,30" transparent="1" backgroundColor="background" font="Prive4;20" foregroundColor="#6cbcf0">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="737,987" size="60,30" font="Prive4;20" foregroundColor="#6cbcf0" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="792,987" size="90,30" transparent="1" backgroundColor="background" font="Prive4;20" foregroundColor="#6cbcf0">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="caidPids" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" transparent="1" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    
  </screen>"""

g17_extraScreen["75"] = """
                                             
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
<ePixmap position="0,818" zPosition="-2" size="1920,495" pixmap="hd_glass17/general/infobar-57.png" alphatest="off" />

	  <widget source="session.CurrentService" render="Label" position="326,858" size="1000,52" font="Prive4;36" halign="left" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">	
    <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>

    <eLabel position="325,981" zPosition="8" size="1525,2" backgroundColor="#1546AF" transparent="0" />
    <eLabel position="70,1018" zPosition="8" size="228,2" backgroundColor="#1546AF" transparent="0" />
    <eLabel position="325,1018" zPosition="8" size="1525,2" backgroundColor="#1546AF" transparent="0" />

    <widget name="TP_type" position="327,987" zPosition="1" size="293,30" font="Prive4;20" halign="left" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />
    <widget name="TP_info" position="737,987" zPosition="2" size="851,30" font="Prive4;20" halign="left" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

    <widget name="Video_size" font="Prive4;18" position="74,1024" size="220,33" halign="center" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />
    <widget name="Prov_temp_rpm" font="Prive4;20" position="1217,987" size="630,37" halign="right" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

    <widget source="global.CurrentTime" render="Label" position="1659,858" size="135,48" font="Prive4;36" valign="top" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1775,861" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="996,869" size="660,33" font="Prive3;27" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1" />
    
    <widget name="g17picon" position="74,871" size="220,132" zPosition="2" transparent="1" alphatest="blend" />

    <widget position="326,908" size="90,39" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" zPosition="1" font="Prive4;24" valign="bottom" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="418,908" size="750,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="-1" font="Prive4;24" valign="bottom" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1138,908" size="142,39" source="session.Event_Now" render="Label" zPosition="1" backgroundColor="background" transparent="1" font="Prive4;24" valign="bottom" foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" backgroundColor="#1546AF" position="325,908" size="957,4" zPosition="3" transparent="0">
      <convert type="EventTime">Progress</convert>
    </widget>

    <widget position="326,937" size="90,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;24" valign="bottom" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="418,937" size="750,39" source="session.Event_Next" render="g17EmptyEpg" backgroundColor="background" transparent="1" font="Prive4;24" valign="bottom" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1138,937" size="142,39" source="session.Event_Next" render="Label" backgroundColor="background" transparent="1" font="Prive4;24" valign="bottom" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    <widget name="Dtype" position="1773,957" size="39,27" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1773,957" size="39,27" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1773,967" size="39,27" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1773,967" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1809,1025" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="702,892" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="702,892" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="702,892" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="702,892" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="702,892" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="702,892" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="702,892" size="39,27" zPosition="3" alphatest="off" />
    
    <widget name="subserv" position="1810,908" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1810,908" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1810,908" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1810,908" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1810,908" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1810,908" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1810,908" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1810,908" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1810,908" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1810,908" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1810,908" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget> 
    <widget name="ecmLineInfo" position="650,1024" size="1300,30" font="Prive4;18" noWrap="1" halign="left" transparent="1" backgroundColor="background" foregroundColor="un99bad6" zPosition="5" />
    <widget name="bitrate_info" position="328,1024" zPosition="1" size="1000,24" font="Prive4;18" noWrap="1" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="5" />
    
    <eLabel text="Snr:dB" font="Prive4;20" position="503,987" size="105,30" foregroundColor="#6cbcf0" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="586,987" size="90,30" font="Prive4;20" transparent="1" backgroundColor="background" zPosition="5" foregroundColor="#6cbcf0">
      <convert type="g17ExtraSource">SnrdB</convert>
    </widget>
    <eLabel text="-" position="643,987" size="60,30" font="Prive4;20" foregroundColor="#6cbcf0" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="660,987" size="90,30" transparent="1" backgroundColor="background" font="Prive4;20" foregroundColor="#6cbcf0">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="caidPids" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" transparent="1" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    
  </screen>"""

g17_extraScreen["76"] = """
                                             
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
<ePixmap position="0,835" zPosition="-2" size="1920,495" pixmap="hd_glass17/general/infobar-57.png" alphatest="off" />

    <eLabel position="300,991" zPosition="8" size="1320,2" backgroundColor="#1546AF" transparent="0" />
    <eLabel position="300,1027" zPosition="8" size="1320,2" backgroundColor="#1546AF" transparent="0" />
    <eLabel position="60,1027" zPosition="8" size="220,2" backgroundColor="#1546AF" transparent="0" />
    <eLabel position="1640,1027" zPosition="8" size="220,2" backgroundColor="#1546AF" transparent="0" />
    <eLabel text="Service Provider" font="Prive4;16" position="1640,1033" size="220,30" halign="center" foregroundColor="#6cbcf0" backgroundColor="background" transparent="1" />

    <widget name="TP_type" position="300,1033" zPosition="1" size="293,30" font="Prive4;16" halign="left" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />
    <widget name="TP_info" position="746,1033" zPosition="2" size="851,30" font="Prive4;16" halign="left" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

    <widget name="Video_size" font="Prive4;16" position="60,1033" size="220,33" halign="center" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />
    <widget name="Prov_temp_rpm" font="Prive4;16" position="302,1033" size="1318,30" halign="right" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

	  <widget source="session.CurrentService" render="Label" position="298,876" size="900,40" font="Prive4;31" halign="left" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">	
    <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>

    <widget source="global.CurrentTime" render="Label" position="1450,876" size="135,48" font="Prive4;31" valign="top" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1551,879" size="69,30" font="Prive4;20" valign="top" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A %d.%B" position="823,882" size="660,33" font="Prive3;27" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1" />
   
    <widget name="g17picon" position="60,884" size="220,132" zPosition="2" transparent="1" alphatest="blend" />
    <widget name="picProvSat" position="1640,884" size="220,132" zPosition="2" transparent="1" alphatest="blend" />
    <widget name="weaTxt" position="1640,884" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />

    <widget position="299,919" size="90,39" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" zPosition="1" font="Prive4;22" valign="bottom" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="385,919" size="650,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="-1" font="Prive4;22" valign="bottom" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1002,919" size="142,39" source="session.Event_Now" render="Label" zPosition="1" backgroundColor="background" transparent="1" font="Prive4;22" valign="bottom" foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" backgroundColor="#1546AF" position="300,920" size="843,4" zPosition="3" transparent="0">
      <convert type="EventTime">Progress</convert>
    </widget>

    <widget position="299,946" size="90,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;22" valign="bottom" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="385,946" size="650,39" source="session.Event_Next" render="g17EmptyEpg" backgroundColor="background" transparent="1" font="Prive4;22" valign="bottom" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1002,946" size="142,39" source="session.Event_Next" render="Label" backgroundColor="background" transparent="1" font="Prive4;22" valign="bottom" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="Dtype" position="1773,997" size="39,27" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1773,997" size="39,27" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1773,997" size="39,27" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1773,997" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1582,997" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="702,997" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="702,997" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="702,997" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="702,997" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="702,997" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="702,997" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="702,997" size="39,27" zPosition="3" alphatest="off" />

    <widget name="subserv" position="1586,920" size="65,65" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1586,920" size="65,65" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1586,920" size="65,65" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1586,920" size="65,65" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1586,920" size="65,65" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1586,920" size="65,65" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1586,920" size="65,65" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1586,920" size="65,65" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1586,920" size="38,65" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1586,920" size="38,65" zPosition="1" alphatest="off" />    
    <widget position="1586,920" size="38,65" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget> 

    <widget name="ecmLineInfo" position="300,998" size="1320,30" font="Prive4;17" noWrap="1" halign="left" transparent="1" backgroundColor="background" foregroundColor="un99bad6" zPosition="5" />
    
    <eLabel text="Snr:dB" font="Prive4;16" position="443,1033" size="105,30" foregroundColor="#6cbcf0" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="506,1033" size="90,30" font="Prive4;16" transparent="1" backgroundColor="background" zPosition="5" foregroundColor="#6cbcf0">
      <convert type="g17ExtraSource">SnrdB</convert>
    </widget>
    <eLabel text="-" position="550,1033" size="60,30" font="Prive4;16" foregroundColor="#6cbcf0" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="565,1033" size="90,30" transparent="1" backgroundColor="background" font="Prive4;16" foregroundColor="#6cbcf0">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="Agc:" position="635,1033" size="60,30" font="Prive4;16" foregroundColor="#6cbcf0" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="678,1033" size="90,30" transparent="1" backgroundColor="background" font="Prive4;16" foregroundColor="#6cbcf0">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>

		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="caidPids" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" transparent="1" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    
  </screen>"""
  
g17_extraScreen["77"] = """
                                             
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
<ePixmap position="0,835" zPosition="-2" size="1920,495" pixmap="hd_glass17/general/infobar-57.png" alphatest="off" />

    <eLabel position="300,991" zPosition="8" size="1320,2" backgroundColor="#1546AF" transparent="0" />
    <eLabel position="300,1027" zPosition="8" size="1320,2" backgroundColor="#1546AF" transparent="0" />
    <eLabel position="60,1027" zPosition="8" size="220,2" backgroundColor="#1546AF" transparent="0" />
    <eLabel position="1640,1027" zPosition="8" size="220,2" backgroundColor="#1546AF" transparent="0" />
    <eLabel text="Service Provider" font="Prive4;16" position="1640,1033" size="220,30" halign="center" foregroundColor="#6cbcf0" backgroundColor="background" transparent="1" />

    <widget name="TP_type" position="300,1033" zPosition="1" size="293,30" font="Prive4;16" halign="left" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />
    <widget name="TP_info" position="625,1033" zPosition="2" size="1004,30" font="Prive4;16" halign="left" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

    <widget name="Video_size" font="Prive4;16" position="60,1033" size="220,33" halign="center" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />
    <widget name="Prov_temp_rpm" font="Prive4;16" position="302,1033" size="1318,30" halign="right" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />

	  <widget source="session.CurrentService" render="Label" position="298,876" size="900,40" font="Prive4;31" halign="left" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">	
    <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>

    <widget source="global.CurrentTime" render="Label" position="1450,876" size="135,48" font="Prive4;31" valign="top" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1551,879" size="69,30" font="Prive4;20" valign="top" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A %d.%B" position="823,882" size="660,33" font="Prive3;27" halign="right" backgroundColor="background" foregroundColor="#DCDCDC" transparent="1" />
     
    <widget name="g17picon" position="60,884" size="220,132" zPosition="2" transparent="1" alphatest="blend" />
    <widget name="picProvSat" position="1640,884" size="220,132" zPosition="2" transparent="1" alphatest="blend" />
    <widget name="weaTxt" position="1640,884" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />

    <widget position="299,919" size="90,39" source="session.Event_Now" render="Label" transparent="1" backgroundColor="background" zPosition="1" font="Prive4;22" valign="bottom" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="385,919" size="650,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" transparent="1" backgroundColor="background" zPosition="-1" font="Prive4;22" valign="bottom" noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1002,919" size="142,39" source="session.Event_Now" render="Label" zPosition="1" backgroundColor="background" transparent="1" font="Prive4;22" valign="bottom" foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" backgroundColor="#1546AF" position="300,920" size="843,4" zPosition="3" transparent="0">
      <convert type="EventTime">Progress</convert>
    </widget>

    <widget position="299,946" size="90,39" source="session.Event_Next" render="Label" transparent="1" backgroundColor="background" font="Prive4;22" valign="bottom" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="385,946" size="650,39" source="session.Event_Next" render="g17EmptyEpg" backgroundColor="background" transparent="1" font="Prive4;22" valign="bottom" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1002,946" size="142,39" source="session.Event_Next" render="Label" backgroundColor="background" transparent="1" font="Prive4;22" valign="bottom" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="Dtype" position="1773,997" size="39,27" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1773,997" size="39,27" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1773,997" size="39,27" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1773,997" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1582,997" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="702,997" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="702,997" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="702,997" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="702,997" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="702,997" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="702,997" size="39,27" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="702,997" size="39,27" zPosition="3" alphatest="off" />

    <widget name="subserv" position="1586,920" size="65,65" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1586,920" size="65,65" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1586,920" size="65,65" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1586,920" size="65,65" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1586,920" size="65,65" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1586,920" size="65,65" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1586,920" size="65,65" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1586,920" size="65,65" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1586,920" size="38,65" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1586,920" size="38,65" zPosition="1" alphatest="off" />    
    <widget position="1586,920" size="38,65" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget> 

    <widget name="ecmLineInfo" position="300,998" size="1320,30" font="Prive4;17" noWrap="1" halign="left" transparent="1" backgroundColor="background" foregroundColor="un99bad6" zPosition="5" />
    
    <eLabel text="Snr:" font="Prive4;16" position="443,1033" size="105,30" foregroundColor="#6cbcf0" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="486,1033" size="90,30" font="Prive4;16" transparent="1" backgroundColor="background" zPosition="5" foregroundColor="#6cbcf0">
      <convert type="g17ExtraSource">SnrdB</convert>
    </widget>
    <eLabel text="-" position="530,1033" size="60,30" font="Prive4;16" foregroundColor="#6cbcf0" backgroundColor="background" transparent="1" />
    <widget source="session.FrontendStatus" render="Label" position="545,1033" size="90,30" transparent="1" backgroundColor="background" font="Prive4;16" foregroundColor="#6cbcf0">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>

		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="caidPids" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" transparent="1" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    
  </screen>"""

g17_extraScreen["87"] = """
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,22" size="1920,1080" backgroundColor="transparent">
<ePixmap position="0,630" zPosition="-1" size="1920,495" pixmap="hd_glass17/general/infobar-30-fs8.png" alphatest="off" />
<ePixmap position="60,870" zPosition="0" size="1800,3" pixmap="hd_glass17/general/blueline.png" />
<ePixmap position="60,961" zPosition="0" size="1800,3" pixmap="hd_glass17/general/blueline.png" />
<widget position="450,672" size="937,52" source="session.CurrentService" render="Label" font="Prive4;42" zPosition="2" valign="center" halign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <widget name="TP_info" position="772,970" zPosition="8" size="1087,60" font="Prive4;40"  valign="center" halign="right" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget name="TP_type" position="1335,672" zPosition="1" size="525,60" font="Prive4;42"  valign="center" halign="right" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget name="Video_size" font="Prive4;42" position="60,672" size="375,60"  valign="center" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1335,742" size="525,60" font="Prive4;42"  valign="center" halign="right" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format:%H:%M:%S</convert>
    </widget>
    <widget name="Prov_temp_rpm" position="1235,804" size="625,60" font="Prive4;38" valign="center" halign="right" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" zPosition="5" transparent="1"  />

    <widget name="Dtype" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    
    <widget source="session.FrontendInfo" render="g17TunersLabel" font="Regular2;43" alphatest="off" position="810,894" size="450,48" tuners="12" ActiveTunerColor="#0000d100" backgroundColor="background" BackgroundActiveTunerColor="#00ecb100" zPosition="4"/>

     <ePixmap position="60,744" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="79,760" size="150,90" zPosition="2" transparent="1" alphatest="on" />
    
    <widget position="258,751" size="225,60" source="session.Event_Now" backgroundColor="background" transparent="1" valign="center" render="Label" zPosition="1" font="Prive4;42" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="399,751" size="703,60" source="session.Event_Now" backgroundColor="background" transparent="1" valign="center" render="g17EmptyEpg" readTagInfo="1" zPosition="2" font="Prive4;42"  noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1102,751" size="225,60" source="session.Event_Now" backgroundColor="background" transparent="1" valign="center" render="Label" zPosition="3" font="Prive4;42"  foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="396,729" size="762,21" zPosition="6" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="396,729" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="5" alphatest="on" />
 
    <widget position="258,807" size="225,60" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="Label" font="Prive4;42"  zPosition="5" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="399,807" size="703,60" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="g17EmptyEpg" font="Prive4;42"  zPosition="6" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1102,807" size="225,60" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="Label" font="Prive4;42"  zPosition="7" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1822,882" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1822,882" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1822,882" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1822,882" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1822,882" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1822,882" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1822,882" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1822,882" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1822,882" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
    <widget name="ecmLineInfo" position="780,994" size="0,0" font="Prive4;18" noWrap="1" halign="right" backgroundColor="background" foregroundColor="unb2e0b4" zPosition="5" />
    <eLabel text="Q:" font="Prive4;40" position="60,970" size="60,50" foregroundColor="green" transparent="1" valign="top" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="120,970" size="200,50" transparent="1" font="Prive4;40" halign="left" valign="top" zPosition="1" backgroundColor="background" foregroundColor="white">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <eLabel text="S:" position="290,970" size="50,50" font="Prive4;40" foregroundColor="yellow" transparent="1" valign="top" backgroundColor="background" />
    <widget source="session.FrontendStatus" render="Label" position="350,970" size="200,50" transparent="1" font="Prive4;40" halign="left" valign="top" backgroundColor="background" foregroundColor="white">
      <convert type="g17ExtraSource">AgcText</convert>
    </widget>
    
		<widget name="ecmlabels" font="Prive3;24" position="108,165" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,165" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget  name="back_enhanced" alphatest="off" position="60,0"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" zPosition="-2" />
    <widget name="picProv" position="120,54"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,54"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,511"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,511"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    
  </screen>"""
  
g17_extraScreen["88"] = """
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,22" size="1920,1080" backgroundColor="transparent">
<ePixmap position="0,630" zPosition="-1" size="1920,495" pixmap="hd_glass17/general/infobar-30-fs8.png" alphatest="off" />
<ePixmap position="60,870" zPosition="0" size="1800,3" pixmap="hd_glass17/general/blueline.png" />
<ePixmap position="60,961" zPosition="0" size="1800,3" pixmap="hd_glass17/general/blueline.png" />
<widget position="450,672" size="937,52" source="session.CurrentService" render="Label" font="Prive4;42" zPosition="2" valign="center" halign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <widget name="TP_info" position="772,970" zPosition="8" size="1087,60" font="Prive4;40"  valign="center" halign="right" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget name="TP_type" position="1335,672" zPosition="1" size="525,60" font="Prive4;42"  valign="center" halign="right" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget name="Video_size" font="Prive4;42" position="60,672" size="375,60"  valign="center" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1335,742" size="525,60" font="Prive4;42"  valign="center" halign="right" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format:%H:%M:%S</convert>
    </widget>
    <widget name="Prov_temp_rpm" position="1235,804" size="625,60" font="Prive4;38" valign="center" halign="right" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" zPosition="5" transparent="1"  />

    <widget name="Dtype" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    
    <widget source="session.FrontendInfo" render="g17TunersLabel" font="Regular2;43" alphatest="off" position="810,894" size="450,48" tuners="12" ActiveTunerColor="#0000d100" backgroundColor="background" BackgroundActiveTunerColor="#00ecb100" zPosition="4"/>

     <ePixmap position="60,744" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="79,760" size="150,90" zPosition="2" transparent="1" alphatest="on" />
    
    <widget position="258,751" size="225,60" source="session.Event_Now" backgroundColor="background" transparent="1" valign="center" render="Label" zPosition="1" font="Prive4;42" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="399,751" size="703,60" source="session.Event_Now" backgroundColor="background" transparent="1" valign="center" render="g17EmptyEpg" readTagInfo="1" zPosition="2" font="Prive4;42"  noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1102,751" size="225,60" source="session.Event_Now" backgroundColor="background" transparent="1" valign="center" render="Label" zPosition="3" font="Prive4;42"  foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="396,729" size="762,21" zPosition="6" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="396,729" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="5" alphatest="on" />
 
    <widget position="258,807" size="225,60" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="Label" font="Prive4;42"  zPosition="5" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="399,807" size="703,60" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="g17EmptyEpg" font="Prive4;42"  zPosition="6" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1102,807" size="225,60" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="Label" font="Prive4;42"  zPosition="7" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1822,882" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1822,882" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1822,882" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1822,882" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1822,882" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1822,882" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1822,882" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1822,882" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1822,882" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
    <widget name="ecmLineInfo" position="780,994" size="0,0" font="Prive4;18" noWrap="1" halign="right" backgroundColor="background" foregroundColor="unb2e0b4" zPosition="5" />
    <widget name="bitrate_info" position="60,970" zPosition="6" size="712,60" font="Prive4;40" noWrap="1" valign="center" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" />

		<widget name="ecmlabels" font="Prive3;24" position="108,165" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,165" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget  name="back_enhanced" alphatest="off" position="60,0"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" zPosition="-2" />
    <widget name="picProv" position="120,54"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,54"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,511"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,511"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    
  </screen>"""
  
g17_extraScreen["89"] = """
  <screen name="ExtraInfo17" flags="wfNoBorder" position="0,22" size="1920,1080" backgroundColor="transparent">
<ePixmap position="0,630" zPosition="-1" size="1920,495" pixmap="hd_glass17/general/infobar-30-fs8.png" alphatest="off" />
<ePixmap position="60,870" zPosition="0" size="1800,3" pixmap="hd_glass17/general/blueline.png" />
<ePixmap position="60,961" zPosition="0" size="1800,3" pixmap="hd_glass17/general/blueline.png" />
<widget position="450,672" size="937,52" source="session.CurrentService" render="Label" font="Prive4;42" zPosition="2" valign="center" halign="center" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <widget name="TP_info" position="772,970" zPosition="8" size="1087,60" font="Prive4;40"  valign="center" halign="right" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget name="TP_type" position="1335,672" zPosition="1" size="525,60" font="Prive4;42"  valign="center" halign="right" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget name="Video_size" font="Prive4;42" position="60,672" size="375,60"  valign="center" halign="left" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1335,742" size="525,60" font="Prive4;42"  valign="center" halign="right" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format:%H:%M:%S</convert>
    </widget>
    <widget name="Prov_temp_rpm" position="1235,804" size="0,0" font="Prive4;38" valign="center" halign="right" noWrap="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" zPosition="5" transparent="1"  />
        <widget source="session.FrontendStatus" render="Label" font="Prive4;42" position="1335,802" size="525,60" zPosition="6" valign="center" halign="right" backgroundColor="background" foregroundColor="orange" transparent="1" >
        <convert type="g17ExtraSource">SnrdB2</convert>
        </widget>
    <widget name="Dtype" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="702,892" size="78,46" zPosition="3" alphatest="off" />
    
    <widget source="session.FrontendInfo" render="g17TunersLabel" font="Regular2;43" alphatest="off" position="810,894" size="450,48" tuners="12" ActiveTunerColor="#0000d100" backgroundColor="background" BackgroundActiveTunerColor="#00ecb100" zPosition="4"/>

     <ePixmap position="60,744" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="79,760" size="150,90" zPosition="2" transparent="1" alphatest="on" />
    
    <widget position="258,751" size="225,60" source="session.Event_Now" backgroundColor="background" transparent="1" valign="center" render="Label" zPosition="1" font="Prive4;42" foregroundColor="unb2e0b4">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="399,751" size="703,60" source="session.Event_Now" backgroundColor="background" transparent="1" valign="center" render="g17EmptyEpg" readTagInfo="1" zPosition="2" font="Prive4;42"  noWrap="1" foregroundColor="unb2e0b4">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1102,751" size="225,60" source="session.Event_Now" backgroundColor="background" transparent="1" valign="center" render="Label" zPosition="3" font="Prive4;42"  foregroundColor="unb2e0b4" halign="right">
      <convert type="g17EventTime">Remaining</convert>
    </widget>

    <widget source="session.Event_Now" render="Progress" pixmap="hd_glass17/slider/slider_main.png" position="396,729" size="762,21" zPosition="6" transparent="1">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="396,729" size="762,21" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="5" alphatest="on" />
 
    <widget position="258,807" size="225,60" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="Label" font="Prive4;42"  zPosition="5" foregroundColor="un99bad6">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <widget position="399,807" size="703,60" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="g17EmptyEpg" font="Prive4;42"  zPosition="6" noWrap="1" foregroundColor="un99bad6">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1102,807" size="225,60" source="session.Event_Next" backgroundColor="background" transparent="1" valign="center" render="Label" font="Prive4;42"  zPosition="7" foregroundColor="un99bad6" halign="right">
      <convert type="g17EventTime">Duration</convert>
    </widget>

    <widget name="subserv" position="1822,882" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1822,882" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1822,882" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1822,882" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1822,882" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1569,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1569,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1822,882" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1822,882" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1822,882" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1822,882" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    
    <widget name="ecmLineInfo" position="780,994" size="0,0" font="Prive4;18" noWrap="1" halign="right" backgroundColor="background" foregroundColor="unb2e0b4" zPosition="5" />
    <widget name="bitrate_info" position="60,970" zPosition="6" size="712,60" font="Prive4;40" noWrap="1" valign="center" halign="left" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="0,0" transparent="1" />

		<widget name="ecmlabels" font="Prive3;24" position="108,165" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,165" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget  name="back_enhanced" alphatest="off" position="60,0"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" zPosition="-2" />
    <widget name="picProv" position="120,54"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,54"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,511"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,511"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget  name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    
  </screen>"""
  
g17_extraScreen["98"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <eLabel position="40,740" zPosition="-2" size="1840,310" backgroundColor="background" transparent="0" />
                                                                     
    <widget source="session.CurrentService" render="Label" position="265,754" size="777,48" font="Prive4;38" noWrap="1" halign="left" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2" valign="bottom">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="987,766" size="660,30" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1659,754" size="135,48" font="Prive4;39" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1775,757" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <eLabel position="265,818" zPosition="8" size="1580,1" backgroundColor="#1546AF" transparent="0" />
    <ePixmap position="61,755" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="80,771" size="150,90" zPosition="2" transparent="1" alphatest="on" />   
     <ePixmap position="61,879" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="80,895" size="150,90" zPosition="2" transparent="1" alphatest="on" /> 
    <widget name="weaTxt" position="80,895" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
      
    <widget name="Prov_temp_rpm" position="1221,826" size="625,33" font="Prive3;27" halign="right" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />
    
    <widget position="265,828" size="90,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <eLabel text="- " font="Prive4;27" position="355,828" size="10,39" halign="left" valign="bottom" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background"/>
    <widget position="371,828" size="90,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">EndTime</convert>
    </widget>
    <widget position="467,828" size="669,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1139,828" size="142,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" halign="right" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" backgroundColor="#1546AF" position="265,882" size="1016,5" zPosition="3" transparent="0">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="265,877" size="0,0" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />    
    <widget position="265,892" size="90,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <eLabel text="- " font="Prive4;27" position="355,892" size="10,39" halign="left" valign="bottom" foregroundColor="un99bad6" transparent="1" backgroundColor="background"/>
    <widget position="371,892" size="90,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">EndTime</convert>
    </widget>
    <widget position="467,892" size="669,39" source="session.Event_Next" render="g17EmptyEpg" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6" transparent="1" backgroundColor="background">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1139,892" size="142,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" halign="right" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    <widget name="subserv" position="1809,871" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1809,871" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1809,871" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1809,871" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1809,871" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1809,871" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1809,871" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1809,871" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1809,871" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1809,871" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1809,871" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    <eLabel position="265,942" zPosition="8" size="1580,1" backgroundColor="#1546AF" transparent="0" />    
    <widget name="TP_type" position="265,951" zPosition="1" size="280,30" font="Prive4;22" halign="left" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget name="TP_info" position="465,951" zPosition="2" size="815,30" font="Prive4;22" halign="left" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />

    <widget name="Dtype" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1773,951" size="78,46" zPosition="3" alphatest="off" />
          	
  	<widget name="Video_size" font="Prive4;20" position="55,1008" size="201,30" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />

    <eLabel text="Snr:" font="Prive4;20" position="265,1008" size="60,30" halign="left" foregroundColor="un99bad6" transparent="1" backgroundColor="background"/>
    <widget source="session.FrontendStatus" render="Label" position="314,1008" size="105,30" font="Prive4;20" halign="left" zPosition="5" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17ExtraSource">SnrdB2</convert>
    </widget>
    <ePixmap pixmap="hd_glass17/slider/sigsnrbar_back43.png" position="265,993" size="230,6" zPosition="1" alphatest="on"/>
  	<widget source="session.FrontendStatus" render="Progress" position="265,993" size="230,6" zPosition="2" pixmap="hd_glass17/slider/sigbar43.png" transparent="1" >
    <convert type="g17ExtraSource">SnrNum</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" position="375,1008" size="105,30" font="Prive4;20" halign="right" zPosition="5" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendInfo" render="g17TunersLabel" font="Regular2;20" PosLR="left" position="824,1009" alphatest="off" size="247,30" zPosition="5" tuners="5" ActiveTunerColor="#0000d100" backgroundColor="background" BackgroundActiveTunerColor="#00ecb100"/>

    <widget name="bitrate_info" position="495,1008" zPosition="4" size="400,30" font="Prive4;19" halign="left" backgroundColor="background" transparent="1"/>    
    <widget name="ecmLineInfo" position="589,1009" size="1258,24" font="Prive4;18" noWrap="1" halign="right" backgroundColor="background" foregroundColor="unb2e0b4" zPosition="6" transparent="1" />

		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>	
    <widget name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    </screen>"""
g17_extraScreen["99"] = """
    <screen name="ExtraInfo17" flags="wfNoBorder" position="0,0" size="1920,1080" backgroundColor="transparent">
    <eLabel position="0,780" zPosition="-2" size="1920,300" backgroundColor="background" transparent="0" />

    <widget source="session.CurrentService" render="Label" position="215,794" size="877,48" font="Prive4;38" noWrap="1" halign="left" transparent="1" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" zPosition="2" valign="bottom">
      <convert type="g17ServiceNum">NumberAndName</convert>
    </widget>
    <widget source="global.CurrentTime" render="g17dateFormat" format="%A  %d.%B %Y" position="1037,806" size="660,30" font="Prive3;27" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <widget source="global.CurrentTime" render="Label" position="1709,794" size="135,48" font="Prive4;39" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Default</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1825,797" size="69,33" font="Prive4;27" valign="top" halign="right" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
      <convert type="g17ClockToText">Format::%S</convert>
    </widget>
    <eLabel position="215,858" zPosition="8" size="1705,1" backgroundColor="#1546AF" transparent="0" />
    <ePixmap position="11,795" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="g17picon" position="30,811" size="150,90" zPosition="2" transparent="1" alphatest="on" />   
     <ePixmap position="11,919" size="189,123" pixmap="hd_glass17/frame_hd.png" zPosition="1" alphatest="off" />
    <widget name="picProvSat" position="30,935" size="150,90" zPosition="2" transparent="1" alphatest="on" /> 
    <widget name="weaTxt" position="30,935" size="75,26" font="Regular2;25" foregroundColor="#00ff8000" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" halign="top" valign="left" zPosition="8" transparent="1" />
      
    <widget name="Prov_temp_rpm" position="1266,866" size="635,33" font="Prive3;27" halign="right" backgroundColor="background" foregroundColor="un99bad6" transparent="1" />
    
    <widget position="215,868" size="90,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <eLabel text="- " font="Prive4;27" position="305,868" size="10,39" halign="left" valign="bottom" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background"/>
    <widget position="321,868" size="90,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">EndTime</convert>
    </widget>
    <widget position="417,868" size="769,39" source="session.Event_Now" render="g17EmptyEpg" readTagInfo="1" zPosition="-1" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1189,868" size="142,39" source="session.Event_Now" render="Label" zPosition="1" font="Prive4;27" valign="bottom" foregroundColor="unb2e0b4" halign="right" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">Remaining</convert>
    </widget>
    <widget source="session.Event_Now" render="Progress" backgroundColor="#1546AF" position="215,922" size="1116,5" zPosition="3" transparent="0">
      <convert type="EventTime">Progress</convert>
    </widget>
    <widget name="slider_back" position="265,877" size="0,0" pixmap="hd_glass17/slider/slider_back-fs8.png" zPosition="2" alphatest="on" />    
    <widget position="215,932" size="90,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">StartTime</convert>
    </widget>
    <eLabel text="- " font="Prive4;27" position="305,932" size="10,39" halign="left" valign="bottom" foregroundColor="un99bad6" transparent="1" backgroundColor="background"/>
    <widget position="321,932" size="90,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">EndTime</convert>
    </widget>
    <widget position="417,932" size="769,39" source="session.Event_Next" render="g17EmptyEpg" font="Prive4;27" valign="bottom" noWrap="1" foregroundColor="un99bad6" transparent="1" backgroundColor="background">
      <convert type="EventName">Name</convert>
    </widget>
    <widget position="1189,932" size="142,39" source="session.Event_Next" render="Label" font="Prive4;27" valign="bottom" foregroundColor="un99bad6" halign="right" transparent="1" backgroundColor="background">
      <convert type="g17EventTime">Duration</convert>
    </widget>
    <widget name="subserv" position="1859,911" size="72,72" pixmap="hd_glass17/icons/i_subw.png" zPosition="1" alphatest="off" />
    <widget name="wide" position="1859,911" size="72,72" pixmaps="hd_glass17/icons/i_formats.png,hd_glass17/icons/i_formatw.png,hd_glass17/icons/hdr.png,hd_glass17/icons/hlg.png" zPosition="1" alphatest="off" />
    <widget name="dolby" position="1859,911" size="72,72" pixmaps="hd_glass17/icons/i_dolbyw.png,hd_glass17/icons/dd5.png,hd_glass17/icons/dd2.png,hd_glass17/icons/mpg.png,hd_glass17/icons/dts.png,hd_glass17/icons/aac.png" zPosition="1" alphatest="off" />
    <widget name="multi_audio" position="1859,911" size="72,72" pixmap="hd_glass17/icons/i_audiow.png" zPosition="1" alphatest="off" />
    <widget name="txt" position="1859,911" size="72,72" pixmap="hd_glass17/icons/i_txtw.png" zPosition="1" alphatest="off" />
    <widget name="hd_sd" position="1859,911" size="72,72" pixmaps="hd_glass17/icons/i_sdw.png,hd_glass17/icons/i_hdw.png,hd_glass17/icons/i_fhd.png,hd_glass17/icons/i_uhd.png,hd_glass17/icons/4k.png,hd_glass17/icons/8k.png" zPosition="1" alphatest="off" />
    <widget name="hbb" position="1859,911" size="72,72" pixmap="hd_glass17/icons/i_hbb.png" zPosition="1" alphatest="off" />
    <widget name="subtit" position="1859,911" size="72,72" pixmap="hd_glass17/icons/i_subtit.png" zPosition="1" alphatest="off" />
    <widget name="tuner" position="1859,911" size="42,72" zPosition="1" alphatest="off" />
    <widget name="HDD_state" position="1859,911" size="42,72" zPosition="1" alphatest="off" />    
    <widget position="1859,911" size="42,72" source="session.RecordState" render="Pixmap" pixmap="hd_glass17/icons/i_rec-n.png" zPosition="2" alphatest="on">
      <convert type="g17ConditionalShowHide">Blink</convert>
    </widget>
    <eLabel position="215,982" zPosition="8" size="1705,1" backgroundColor="#1546AF" transparent="0" />    
    <widget name="TP_type" position="215,991" zPosition="1" size="280,30" font="Prive4;22" halign="left" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />
    <widget name="TP_info" position="415,991" zPosition="2" size="815,30" font="Prive4;22" halign="left" foregroundColor="un99bad6" transparent="1" backgroundColor="background" />

    <widget name="Dtype" position="1823,991" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dcam" position="1823,991" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Decm" position="1823,991" size="78,46" zPosition="3" alphatest="off" />
    <widget name="Dnetstate" position="1823,991" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D1_Demm" pixmap="hd_glass17/icons/irdemm-fs8.png" position="1823,991" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D2_Demm" pixmap="hd_glass17/icons/secemm-fs8.png" position="1823,991" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D3_Demm" pixmap="hd_glass17/icons/nagemm-fs8.png" position="1823,991" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D4_Demm" pixmap="hd_glass17/icons/viaemm-fs8.png" position="1823,991" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D5_Demm" pixmap="hd_glass17/icons/conemm-fs8.png" position="1823,991" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D0_Demm" pixmap="hd_glass17/icons/betemm-fs8.png" position="1823,991" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D6_Demm" pixmap="hd_glass17/icons/crwemm-fs8.png" position="1823,991" size="78,46" zPosition="3" alphatest="off" />
    <widget name="D7_Demm" pixmap="hd_glass17/icons/drcemm-fs8.png" position="1823,991" size="78,46" zPosition="3" alphatest="off" />
          	
  	<widget name="Video_size" font="Prive4;20" position="5,1048" size="201,30" halign="center" backgroundColor="un353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />

    <eLabel text="Snr:" font="Prive4;20" position="215,1048" size="60,30" halign="left" foregroundColor="un99bad6" transparent="1" backgroundColor="background"/>

    <widget source="session.FrontendStatus" render="Label" position="264,1048" size="105,30" font="Prive4;20" halign="left" zPosition="5" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17ExtraSource">SnrdB2</convert>
    </widget>
    <ePixmap pixmap="hd_glass17/slider/sigsnrbar_back43.png" position="215,1033" size="230,6" zPosition="1" alphatest="on"/>

  	<widget source="session.FrontendStatus" render="Progress" position="215,1033" size="230,6" zPosition="2" pixmap="hd_glass17/slider/sigbar43.png" transparent="1" >
    <convert type="g17ExtraSource">SnrNum</convert>
    </widget>
    <widget source="session.FrontendStatus" render="Label" position="325,1048" size="105,30" font="Prive4;20" halign="right" zPosition="5" foregroundColor="unb2e0b4" transparent="1" backgroundColor="background">
      <convert type="g17ExtraSource">SnrText</convert>
    </widget>
    <widget source="session.FrontendInfo" render="g17TunersLabel" font="Regular2;20" PosLR="left" position="774,1049" alphatest="off" size="247,30" zPosition="5" tuners="5" ActiveTunerColor="#0000d100" backgroundColor="background" BackgroundActiveTunerColor="#00ecb100"/>

    <widget name="bitrate_info" position="445,1048" zPosition="4" size="400,30" font="Prive4;19" halign="left" backgroundColor="background" transparent="1"/>    
    <widget name="ecmLineInfo" position="619,1049" size="1268,24" font="Prive4;18" noWrap="1" halign="right" backgroundColor="background" foregroundColor="unb2e0b4" zPosition="6" transparent="1" />

		<widget name="ecmlabels" font="Prive3;24" position="108,225" zPosition="2" size="150,361" backgroundColor="background" foregroundColor="unb2e0b4" transparent="1" />
		<widget name="ecmValues" font="Prive3;24" position="190,225" zPosition="3" size="318,361" backgroundColor="background" transparent="1" />
    <widget name="back_enhanced" position="60,60"  size="465,660" pixmap="hd_glass17/menu/back_enhanced-fs8.png" alphatest="off" zPosition="0" />
    <widget name="picProv" position="120,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="picSat" position="318,114"  size="150,90"  zPosition="1" alphatest="on"/>
    <widget name="piconEcm" position="120,572"  size="150,90"  zPosition="2" alphatest="on"/>
    <widget name="piconCam" position="318,572"  size="150,90"  zPosition="2" alphatest="on"/>	
    <widget name="caidPids" transparent="1" position="1639,105" zPosition="1" size="195,600" font="Prive4;21" halign="center" foregroundColor="white" backgroundColor="background" />
    <widget name="caidPids_back" position="1609,45"  size="255,600" pixmap="hd_glass17/menu/back_caidPids-fs8.png" alphatest="off" zPosition="0" />
    <widget name="active_caidPid" transparent="1" position="1639,105" zPosition="2" size="195,25" font="Prive4;21" halign="center" foregroundColor="#00d100" backgroundColor="background" />
    <widget name="caidPids_end" position="1609,115"  size="255,30" pixmap="hd_glass17/menu/end_caidPids-fs8.png" alphatest="off" zPosition="3" />
    </screen>"""  
