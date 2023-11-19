# bpgbatch
Decode multiple bpg images at the same time with a python script

You need to self-download bpg decoder from [here](https://bellard.org/bpg/) and put the script under the same folder as `bpgdec.exe`.

Then run the script like:

```shell
python bpgbatch.py {folder}
```

The script will get all bpg files (end up with `.bpg`) under the target folder and call `bpgdec.exe` to decode them. Outputs will be dumped under `output/`.

If the filename of the bpg file contains unicode-characters that cannot be recognized by `bpgdec.exe` (it does happen), the script will automatically create a copy of the file with a filename that all characters, which cannot be encoded under your system encoding format, will be erased, and hand the copy to `bpgdec.exe` and retry.
