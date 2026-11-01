# -*- coding: utf-8 -*-
"""Optional bounded receiver diagnostics, disabled in the stable build."""
import hashlib
import json
import os
import time

PATH = '/tmp/fullhdglass-bitrate.json'
LIMIT = 24
DIAGNOSTICS_ENABLED = False

class BitrateDiagnostic(object):
    def __init__(self, video_pid, audio_pid, argv, streamdata, path=PATH):
        self.enabled = DIAGNOSTICS_ENABLED
        self.path = path
        self.events = []
        self.started = time.time()
        self.data = {'build':'1.0.55', 'cpu':os.uname()[4],
                     'video_pid':video_pid, 'audio_pid':audio_pid,
                     'argv':argv, 'stream':self.stream_fields(streamdata), 'events':self.events}
        if not self.enabled:
            return
        try:
            with open(argv[0], 'rb') as helper:
                self.data['helper_sha256'] = hashlib.sha256(helper.read()).hexdigest()
        except Exception as error:
            self.data['helper_error'] = str(error)[:160]
        self.record('launch')

    @staticmethod
    def stream_fields(data):
        if not isinstance(data, dict):
            return {'available':False}
        return {key:data[key] for key in ('adapter','demux','pids','video','audio') if key in data}

    def record(self, event, **fields):
        if not self.enabled or len(self.events) >= LIMIT:
            return
        try:
            fields.update(event=event, seconds=round(time.time()-self.started,3))
            self.events.append(fields)
            # Retain the old file if an interrupted write fails. No service URL,
            # credentials, decoded media or transport packets are collected.
            encoded = json.dumps(self.data, ensure_ascii=True, indent=2, default=lambda value:str(value)[:160])
            with open(self.path+'.part', 'w') as output:
                output.write(encoded)
            os.chmod(self.path+'.part',0o600)
            os.rename(self.path+'.part',self.path)
        except Exception:
            pass

    def sample(self, video, audio, service, keys):
        if not self.enabled or len(self.events) >= LIMIT:
            return
        fields = {'video':video, 'audio':audio}
        try:
            info = service and service.info()
            if info:
                fields['video_pid_now'] = info.getInfo(keys.sVideoPID)
                fields['audio_pid_now'] = info.getInfo(keys.sAudioPID)
            stream = service and service.stream()
            if stream:
                fields['stream_now'] = self.stream_fields(stream.getStreamingData())
        except Exception as error:
            fields['metadata_error'] = str(error)[:160]
        self.record('sample', **fields)
