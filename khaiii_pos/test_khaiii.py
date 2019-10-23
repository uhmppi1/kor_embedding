import khaiii
api = khaiii.KhaiiiApi()
api.open()

while True:
    print("KHAIII에 테스트할 문장을 입력해 주세요. 종료하려면 X를 입력해 주세요.")
    var = input("입력: ")
    if str(var) == "X":
        print("테스트를 종료합니다.")
        break
    for word in api.analyze(str(var)):
        morphs_str = ' + '.join([(m.lex + '/' + m.tag) for m in word.morphs])
        print(f'{word.lex}\t{morphs_str}')
    print("\n")
