# smoke_screen
I had this idea about doing fft of live traffic shape, and possibly detecting some isochronous protocol fingerprints.
In case such fingerprints exist, trying to mask the dominant (probably very high) frequencies with additive noise wave in real time seems like a nice project.

# sniffer.py
In this file we run asynchronous sniffer and plot an fft of aggregated traffic, for some aggregation window (e.g. 10-20 ms), for some analysis window (e.g. 1024-4096 aggregation periods). In theory, for isochronous traffic we should see some dominating frequencies and some cute noise for anything else.

# fourier.py
A demo of how the screening should work. For the traffic, we use some sin wave with noise, that obviously does have a dominating frequency. We then detect this frequency and produce frequency-reducing additive noise. It's moderately effective, as the frequency survives, but is not nearly as dominant as before. Six live plots are provided:
* The original traffic
* fft of the original traffic
* The dominant frequencies only
* The calculated additive noise
* The result traffic
* fft of the result traffic