# XTR
The XTR the "Xander Tone Rating" based off of the standard deviation of the overtone series of a note being played.
There are three different specifications within the rating:
- Depth of Sound
  - Determined by the standard deviation of the overtone series
- Brightness of Sound
  - Determined by the average standard deviations of the overtone series with weights on the louder overtones.
- Envelope of Sound
  - Determined by the standard deviation of the derivative (or second derivative) of the graph of a bezier curve plotted
    onto the overtone series
## Developer Log
### Entry 1: December 14, 2024
The figure below is a spectrogram of a saxophone recording being played. Below the initial spectrogram, you can see the
notes detected at that specific time. I am going to add three more graphs that show the three specifications of Tone
Rating.
![img.png](img.png)