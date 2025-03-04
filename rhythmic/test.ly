\version "2.24.4" % Ensure you're using the correct version

music = {
  \time 4/4
  c'4 d'4 e'4 f'4
}

\score {
  \new Staff {
    \clef treble
    \music
  }
}