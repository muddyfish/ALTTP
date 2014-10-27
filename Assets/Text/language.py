import glob, struct

class Text():
  def __init__(self, raw_data):
    self.id = raw_data[0]
    self.textbox = raw_data[1]/16
    self.y_pos = raw_data[1]%16
    self.banks = {"nes": raw_data[2]}
    self.offsets = {"nes": raw_data[3]>>8}
    self.text = {"nes": "Unused"}
    self.set_language("nes")
    
  def __str__(self):
    return self.text[self.language].replace("\x01", "\n").replace("\x02", "\n----\n")  

  def set_language(self, lang):
    self.language = lang
    
  def add_offset(self, lang, offset, bank):
    self.text[lang] = "Unused"
    self.offsets[lang] = offset
    self.banks[lang] = bank
    
  def add_text(self, text_files, text_obj):
    for lang in self.offsets.keys():
      text_files[lang].seek(self.offsets[lang])
      self.text[lang] = text_files[lang].read(text_obj.offsets[lang] - self.offsets[lang])
    
  def get_location(self):
    return{"00": "Items",
	   "01": "Navi",
	   "02": "Talking Doors",
	   "03": "Signs",
	   "04": "Gossip Stones",
	   "06": "Z-Target C-Up Navi",
	   "08": "Ocarina",
	   "10": "Kokiri Forest",
	   "20": "Hyrule Field, Owl",
	   "30": "Death Mountain",
	   "40": "Lake Hylia",
	   "50": "Kakariko, Graveyard",
	   "60": "Gerudo",
	   "70": "Castle",
	   "71": "Mask",
	   "ff": "Padding"}[("%04x" % self.id)[:-2]]

class Language():
  def __init__(self, lang = "nes"):
    raw = glob.glob("Assets/Text/*_message_data_static.zdata")
    self.languages = dict(zip([i.split("/")[-1][:3] for i in raw], [open(i) for i in raw]))
    self.lang = lang
    self.entry_table_obj = open("Assets/Text/text_table.zdata")
    self.load_languages()
    for language in self.languages.values():
      language.close()
    
  def __str__(self):
    return "\n".join(map(str, self.text_objs))
  
  def set_language(self, lang):
    for i in range(len(self.text_objs)-1):
      self.text_objs[i].set_language(lang)
    
  def load_languages(self):
    self.text_objs = []

    raw_data = struct.unpack(">HBxBI", self.entry_table_obj.read(8)+"\x00")
    self.text_objs.append(Text(raw_data))
    while raw_data[0] != 0xFFFF:
      raw_data = struct.unpack(">HBxBI", self.entry_table_obj.read(8)+"\x00")
      self.text_objs.append(Text(raw_data))

    for lang in self.languages.keys():
      if lang == "nes": continue
      for i in range(len(self.text_objs)):
	raw_data = struct.unpack(">BI", self.entry_table_obj.read(4)+"\x00")
	self.text_objs[i].add_offset(lang, raw_data[1], raw_data[0])
    
    for i in range(len(self.text_objs)-1):
      self.text_objs[i].add_text(self.languages, self.text_objs[i+1])
  
if __name__ == "__main__":
  text = Language()
  print text