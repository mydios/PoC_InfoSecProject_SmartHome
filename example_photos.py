from SmartService import SmartService
photo = str('PHOTO_OF_A_FLOWER')
s = SmartService(('localhost', 10007), 'photo_gallery', 15, photo)
s.start()