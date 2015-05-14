**duvet** - A ~~shitty~~ POC mutation based python fuzzer

Can fuzz arbitrary binaries by mutating samples, provided you write a python `Target` subclass that feeds the randomized input into the target and monitors its output.

Small samples files should be favored in order to limit mutating data outside the headers, since this is a lot less likely to cause crashes.

This started out as wanting to automatically prove that the bundled code (`bitmap.c`) was buggy as hell. A noble cause, which led to more buggy code. 