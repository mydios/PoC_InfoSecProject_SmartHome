from SmartService import SmartService
photo = str('THIS_IS_A_PHOTO').encode('utf-8').hex()
s = SmartService(('localhost', 10007), 'photo_gallery', 15, photo)
s.start()