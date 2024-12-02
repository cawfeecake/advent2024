{
  safe++
  if (NF > 1) {
    directionKnown = 0
    isIncreasing = 0
    prev = $1
    for (i = 2; i <= NF; i++) {
      if (directionKnown == 0) {
        if (prev < $i) {
          isIncreasing = 1
        } else if (prev > $i) {
          isIncreasing = 0
        } else {
          safe--
          break
        }
        directionKnown = 1  
      }

      if (isIncreasing == 1 && (prev >= $i || $i > prev + 3)) {
        safe--
        break
      } else if (isIncreasing == 0 && (prev <= $i || $i < prev - 3)) {
        safe--
        break
      }
      prev = $i
    }
  }
}

END {
  print "Safe records:", safe
}
