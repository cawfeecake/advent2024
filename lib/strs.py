def is_palindrome(s: str) -> bool:
    front, back = s[:(len(s) + 1)//2], s[(len(s) + 1)//2:][::-1]
    for i in range(len(back)):
        if front[i] != back[i]:
            return False
    return True
