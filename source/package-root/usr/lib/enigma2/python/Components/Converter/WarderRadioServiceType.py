"""Display the actual radio transport instead of mislabelling its provider."""
from Components.Converter.Converter import Converter
from Components.Element import cached
import NavigationInstance


class WarderRadioServiceType(Converter):
    def __init__(self, kind):
        Converter.__init__(self, kind)
        self.kind=kind

    @cached
    def getText(self):
        if self.kind in ('Lyrics','Radio'):
            from Components.Language import language
            code=language.getLanguage().split('_')[0]
            if self.kind == 'Radio':return 'RÁDIO' if code in ('sk','cs') else 'RADIO'
            return {'sk':'Text piesne','cs':'Text písně','de':'Liedtext','hu':'Dalszöveg',
                    'ru':'Текст песни','fr':'Paroles','it':'Testo della canzone',
                    'es':'Letra de la canción','pl':'Tekst piosenki','uk':'Текст пісні'}.get(code,'Lyrics')
        from enigma import eServiceReference, iServiceInformation
        try:
            nav=NavigationInstance.instance
            ref=nav and nav.getCurrentlyPlayingServiceReference()
            if ref is None:return ''
            if ref.type == getattr(eServiceReference,'idServiceDAB',-1):return 'DAB'
            if ref.type in (4097,5001,5002,8193):return 'IPTV'
            service=nav.getCurrentService();info=service and service.info()
            data=info and info.getInfoObject(iServiceInformation.sTransponderData)
            tuner=str((data or {}).get('tuner_type','')).upper()
            for name in ('DVB-S','DVB-T','DVB-C'):
                if tuner.startswith(name):return name
            return 'RADIO'
        except Exception:return ''
    text=property(getText)
