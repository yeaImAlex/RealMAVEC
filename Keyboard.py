import keyboardM

class Keyboard1:
    def __init__(self):
        keyboardM.init()
        self.win = keyboardM.display.set_mode((100,100))

    def getKey(self, keyName):
        ans = False
        for eve in keyboardM.event.get(): pass
        keyInput = keyboardM.key.get_pressed()
        myKey = getattr(keyboardM, 'K_{}'.format(keyName))
        if keyInput[myKey]:
            ans = True
        keyboardM.display.update()

        return ans

    def main(self):
        if self.getKey('a'):
            print('Left')
        if self.getKey('d'):
            print('Right')
        if self.getKey('w'):
            print('Forward')
        if self.getKey('s'):
            print('Backward')
        if self.getKey('e'):
            print('Right forward')
        if self.getKey('q'):
            print('Left forward')

if __name__ == '__main__':
        keyboard = Keyboard1()

        while True:
           keyboard.main()
    
