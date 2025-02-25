import nlpaug.augmenter.word as naw
import nlpaug.augmenter.char as nac
from transformers import MarianMTModel, MarianTokenizer

class DataAugmentation:
    def __init__(self):
        """Khởi tạo các bộ tăng cường dữ liệu NLP"""
        self.synonym_aug = naw.SynonymAug(aug_src="wordnet")  # Thay từ đồng nghĩa
        self.swap_aug = naw.RandomWordAug(action="swap")  # Đảo vị trí từ
        self.delete_aug = naw.RandomWordAug(action="delete")  # Xóa từ
        self.insert_aug = naw.RandomWordAug(action="insert")  # Thêm từ ngẫu nhiên (cần xem lại thêm)

        # Khởi tạo mô hình dịch ngược (en → de → en)
        self.translator_en_de = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-de")
        self.tokenizer_en_de = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-de")

        self.translator_de_en = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-de-en")
        self.tokenizer_de_en = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-de-en")

    def synonym_augmentation(self, text):
        """Thay thế từ đồng nghĩa"""
        return self.synonym_aug.augment(text)

    def swap_words(self, text):
        """Hoán đổi vị trí từ"""
        return self.swap_aug.augment(text)

    def delete_words(self, text):
        """Xóa từ ngẫu nhiên"""
        return self.delete_aug.augment(text)

    def insert_words(self, text):
        """Thêm từ ngẫu nhiên vào văn bản"""
        return self.insert_aug.augment(text)

    def back_translation(self, text):
        """Dịch ngược bằng mô hình Helsinki-NLP"""
        # Dịch từ Anh -> Đức
        tokens = self.tokenizer_en_de(text, return_tensors="pt", padding=True, truncation=True)
        translated = self.translator_en_de.generate(**tokens)
        translated_text = self.tokenizer_en_de.batch_decode(translated, skip_special_tokens=True)[0]

        # Dịch từ Đức -> Anh
        tokens = self.tokenizer_de_en(translated_text, return_tensors="pt", padding=True, truncation=True)
        back_translated = self.translator_de_en.generate(**tokens)
        back_translated_text = self.tokenizer_de_en.batch_decode(back_translated, skip_special_tokens=True)[0]

        return back_translated_text

augmenter = DataAugmentation()
