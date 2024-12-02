# assumes that NF >= 2

function check_row(skip_i) {
  direction_known = 0
  is_increasing = 0

  if (skip_i == 0) {
    prev = $2
    for (i = 3; i <= NF; i++) {
      # Direction determination...
      if (direction_known == 0) {
        if (prev < $i) {
          is_increasing = 1
          direction_known = 1  
        } else if (prev > $i) {
          is_increasing = 0
          direction_known = 1  
        } else {
          return 0
        }
      }
      # Check condition...
      if (is_increasing == 1 && (prev >= $i || $i > prev + 3)) {
        return 0
      } else if (is_increasing == 0 && (prev <= $i || $i < prev - 3)) {
        return 0
      }

      prev = $i
    }
  } else {
    prev = $1
    for (i = 2; i <= NF; i++) {
      if (skip_i != i) {
        # Direction determination...
        if (direction_known == 0) {
          if (prev < $i) {
            is_increasing = 1
            direction_known = 1  
          } else if (prev > $i) {
            is_increasing = 0
            direction_known = 1  
          } else {
            return 0
          }
        }

        # Check condition...
        if (is_increasing == 1 && (prev >= $i || $i > prev + 3)) {
          return 0
        } else if (is_increasing == 0 && (prev <= $i || $i < prev - 3)) {
          return 0
        }

        prev = $i
      }
    }
  }

  return 1
}

{
  for (outer_i = -1; outer_i <= NF; outer_i++) {
    is_safe = check_row(outer_i)
    if (is_safe > 0) {
      safe++
      break
    }
  }
}

END {
  print "Safe records:", safe
}
