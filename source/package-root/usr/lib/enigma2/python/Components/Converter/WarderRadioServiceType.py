"""Display the actual radio transport instead of mislabelling its provider."""
from Components.Converter.Converter import Converter
from Components.Element import cached
import NavigationInstance
from time import localtime


WEEKDAYS = {
    'sk':('Pondelok','Utorok','Streda','Štvrtok','Piatok','Sobota','Nedeľa'),
    'cs':('Pondělí','Úterý','Středa','Čtvrtek','Pátek','Sobota','Neděle'),
    'de':('Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag'),
    'hu':('Hétfő','Kedd','Szerda','Csütörtök','Péntek','Szombat','Vasárnap'),
    'ru':('Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье'),
    'fr':('Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche'),
    'it':('Lunedì','Martedì','Mercoledì','Giovedì','Venerdì','Sabato','Domenica'),
    'es':('Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'),
    'pl':('Poniedziałek','Wtorek','Środa','Czwartek','Piątek','Sobota','Niedziela'),
    'uk':('Понеділок','Вівторок','Середа','Четвер','П’ятниця','Субота','Неділя'),
    'en':('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')}


def radio_date(timestamp, code):
    if timestamp is None:return ''
    value = localtime(timestamp)
    day = WEEKDAYS.get(code.split('_')[0],WEEKDAYS['en'])[value.tm_wday]
    return '%s %02d.%02d.%04d' % (day,value.tm_mday,value.tm_mon,value.tm_year)


class WarderRadioServiceType(Converter):
    def __init__(self, kind):
        Converter.__init__(self, kind)
        self.kind=kind

    @cached
    def getText(self):
        if self.kind == 'RadioMode':
            from Plugins.Extensions.setupGlass17.warderUiText import ui_text
            return ui_text('Radio mode').upper()
        if self.kind == 'Date':
            from Components.Language import language
            return radio_date(self.source.time,language.getLanguage())
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
