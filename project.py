import re
import hashlib
import hmac
from Crypto.Cipher import AES
import base64
import os
import rsa
from cryptography.fernet import Fernet


class Dil_kontrol:
    def __init__(self,metin):
        if  re.search("[_@$]",metin):
            raise Exception('metin alpha numeric karakter içermemelidir')
        elif re.search("[0-9]",metin):
            raise Exception("metnin içinde rakam olmasın")
        else:
            self.metin=metin

    def Cumle_Ayirma(self):
        result=self.metin.strip()
        result=result.split(".")
        return len(result)-1

    def Kelime_Ayirma(self):
        result=self.metin.strip()
        result=result.replace("."," ")
        result=result.replace(","," ")
        result=result.split(" ")
        return len(result)-1

    def SesliHarf(self):
        sesliHarf="AaEeIıİiOoÖöUuÜü"
        sayac=0
        for i in self.metin:
            if i in sesliHarf:
                sayac=sayac+1
        return sayac

    def BuyukUnlu_Uyumu(self):
        kalınUnlu="AaIıOoUu"
        inceUnlu="EeİiÖöÜü"
        pozSayac=0
        negSayac=0
        result=self.metin.replace(","," ")
        result=result.replace("."," ")
        result=result.split(" ")
        for i in result:
            a=0
            b=0
            for j in i:
                if j in kalınUnlu:
                    a=a+1
                elif j in inceUnlu:
                    b=b+1
            if (a>=1 and b>=1) or a+b==1:
                negSayac=negSayac+1
            if ((a>0 and b==0) or (b>0 and a==0)) and a+b!=1:
                pozSayac=pozSayac+1
        return f"uyan:{pozSayac} uymayan:{negSayac}"
import pypyodbc
class SifrelemeYontemleri:
    def __init__(self,sifrelenecekMetin):
        self.sifrelenecekMetin=sifrelenecekMetin
        self.db = pypyodbc.connect(
        'Driver={SQL Server};'
        'Server=DESKTOP-Q5VTMMT;'
        'Database=proje_final;'
        'Trusted_Connection=True;'
    )
    def sql_connect(self,şifrelenen_metin,algoritma_adı):
        imlec=self.db.cursor()
        imlec.execute('insert into sifrelenmis_metin values(?,?,?,?)',(şifrelenen_metin,algoritma_adı,'py',1))
        self.db.commit()
    def sha256(self):
        sonuc = hashlib.sha256(self.sifrelenecekMetin.encode())
        hashliMetin = sonuc.hexdigest()
        self.sql_connect(hashliMetin,'sha-256')
        print(hashliMetin)
              
    def sha512(self):
        sonuc = hashlib.sha512(self.sifrelenecekMetin.encode())
        hashliMetin = sonuc.hexdigest()
        self.sql_connect(hashliMetin,'sha-512')
        print(hashliMetin)

    def sha224(self):
        sonuc = hashlib.sha224(self.sifrelenecekMetin.encode())
        hashliMetin = sonuc.hexdigest()
        self.sql_connect(hashliMetin,'sha-224')
        print(hashliMetin)

    def md5(self):
        sonuc = hashlib.md5(self.sifrelenecekMetin.encode())
        hashliMetin = sonuc.hexdigest()
        self.sql_connect(hashliMetin,'md-5')
        print(hashliMetin)

    def blake2b(self):
        sonuc = hashlib.blake2b(self.sifrelenecekMetin.encode())
        hashliMetin = sonuc.hexdigest()
        self.sql_connect(hashliMetin,'blank2b')
        print(hashliMetin)

    def blanke2s(self):
        sonuc = hashlib.blake2s(self.sifrelenecekMetin.encode())
        hashliMetin = sonuc.hexdigest()
        self.sql_connect(hashliMetin,'blank2s')
        print(hashliMetin)

    def createRsaKey(self):
        (publicKey, privateKey) = rsa.newkeys(1024)
        return publicKey, privateKey

    def rsaKripto(self):
        publickey, privatekey = self.createRsaKey()
        arr = bytes(self.sifrelenecekMetin, 'utf-8')
        sifre = rsa.encrypt(arr, publickey)
        self.sql_connect(sifre,'rsa')
        return sifre,privatekey

    def rsaDecrypt(self):
        sifreliMetin,privateKey=self.rsaKripto()
        print(sifreliMetin)
        cozulmusMetin=rsa.decrypt(sifreliMetin,privateKey)
        print(cozulmusMetin)

    def fernetKripto(self):
        bytArray=bytes(self.sifrelenecekMetin,  "utf-8")
        key = Fernet.generate_key()
        f = Fernet(key)
        token = f.encrypt(bytArray)
        self.sql_connect(token,'ferned')
        return token,f

    def fernetDecrypt(self):
        token,f=self.fernetKripto()
        print(token)
        acikMetin=f.decrypt(token)
        print(acikMetin.decode("utf-8"))

class Help:
    def help(self,deger=" "):
        if deger==" ":
            print("class:Dil_Kontrol")
            print("--Bu class içinde kullanıcıdan alınan metin üzerinde belli başlı işlemler yapılır")
            print("-----def CumleAyirma\n     +Girdiğiniz metnin içindeki cümle sayısını döndürür.")
            print("-----def KelimeAyirma\n    +Girdiğiniz metni içindeki kelime sayısını döndürür.")
            print("-----def SesliHarf\n     +Girdiğiniz metnin içindeki sesli harf sayısını döndürü")
            print("-----def BuyukUnlu_Uyumu\n     +Girdiğiniz metnin kelimelerinin büyük ünlü uyumuna uyanların ve uymayanların sayısını döndürür.")  
            print("class:SifrelemeYontemleri")
            print("--Bu class string olarak aldığı ifadeyi farklı hashleme ve şifreleme algoritamları kullanarak şifreleyen ve çözen metotlar barındırır.")
            print("-----def sql_connect\n         +sql server'a şifrelenen metinleri gönderen fonksiyondur")
            print("-----def sha256\n           +String olarak aldığı ifadeyi sha-256 algoritması kullanarak hashler.")
            print("-----def sha512\n           +String olarak aldığı ifadeyi sha-512 algoritması kullanarak hashler.")
            print("-----def sha224\n           +String olarak aldığı ifadeyi sha-224 algoritması kullanarak hashler.")
            print("-----def md5\n            +String olarak aldığı ifadeyi md-5 algoritması kullanarak hashler.")
            print("-----def blanke2b\n           +String olarak aldığı ifadeyi blanke2b algoritması kullanarak hashler.")
            print("-----def blanke2s\n           +String olarak aldığı ifadeyi blanke2s algoritması kullanarak hashler.")
            print("-----def createRsaKey\n           +RSA şifreleme algoritması için anahtar üretir")
            print("-----def rsaKripto\n           +String olarak aldığı ifadeyi RSA algoritmasına göre şifreler")
            print("-----def rsaDecrypt\n           +RSA algoritması kullanılarak şifrelenen metni anahtar kullanarak eski haline döndürür.")
            print("-----def fernetKripto\n           +String olarak aldığı ifadeyi simetrik bir şekilde şifreler.")
            print("-----def fernetDecrypt\n           +Fernet ile şifrelenen metni anahtar kullanarak eski haline döndürür.")

        elif deger=="Dil_Kontrol":
            print("<class>")
            print("Bu class kullanıcıdan alınan metin üzerinde belli başlı işlemler yapar")
            print("İçindeki fonksiyonlar:")
            print("<CumleAyirma>","<KelimeAyirma>","<SesliHarf>","<BuyukUnlu_Uyumu>")
        elif deger==("CumleAyirma"):
            print("<def>")
            print("Girdiğiniz metnin içindeki cümle sayısını döndüren fonksiyondur")
        elif deger==("KelimeAyirma"):
            print("<def>")
            print("Girdiğiniz metnin içindeki kelime sayısını döndüren fonksiyondur")
        elif deger==("SesliHarf"):
            print("<def>")
            print("Girdiğiniz metnin içindeki sesli harf sayısını döndüren fonksiyondur")
        elif deger==("BuyukUnlu_Uyumu"):
            print("<def>")
            print("Girdiğiniz metnin kelimelerinin büyük ünlü uyumuna uyanların ve uymayanların sayısını döndüren fonksiyondur.")
        elif deger==("SifrelemeYontemleri"):
            print("Bu class string olarak aldığı ifadeyi farklı hashleme ve şifreleme algoritamları kullanarak şifreleyen ve çözen metotlar barındırır.")
            print("İçindeki fonksiyonlar:")
            print("<sql_connect>,<sha256>","<sha512>","<sha224>","<md5>","<blanke2b>","<blanke2s>","<createRsaKey>","<rsaKripto>","<rsaDecrypt>","<fernetKripto>","<fernetDecrypt>")
        elif deger==("sql_connect"):
            print("<def>")
            print("sql server'a şifrelenmiş metni gönderir")
        elif deger==("sha256"):
            print("<def>")
            print("String olarak aldığı ifadeyi sha-256 algoritması kullanarak hashler.")
        elif deger==("sha512"):
            print("<def>")
            print("String olarak aldığı ifadeyi sha-512 algoritması kullanarak hashler.")
        elif deger==("sha224"):
            print("<def>")
            print("String olarak aldığı ifadeyi sha-224 algoritması kullanarak hashler.")
        elif deger==("md5"):
            print("<def>")
            print("String olarak aldığı ifadeyi md-5 algoritması kullanarak hashler.")
        elif deger==("blanke2b"):
            print("<def>")
            print("String olarak aldığı ifadeyi blanke2b algoritması kullanarak hashler.")
        elif deger==("blanke2s"):
            print("<def>")
            print("String olarak aldığı ifadeyi blanke2s algoritması kullanarak hashler.")
        elif deger==("createRsaKey"):
            print("<def>")
            print("RSA şifreleme algoritması için anahtar üretir")
        elif deger==("rsaKripto"):
            print("<def>")
            print("String olarak aldığı ifadeyi RSA algoritmasına göre şifreler.")
        elif deger==("rsaDecrypt"):
            print("<def>")
            print("RSA algoritması kullanılarak şifrelenen metni anahtar kullanarak eski haline döndürür.")
        elif deger==("fernetKripto"):
            print("<def>")
            print("String olarak aldığı ifadeyi simetrik bir şekilde şifreler.")
        elif deger==("fernetDecrypt"):
            print("<def>")
            print("Fernet ile şifrelenen metni anahtar kullanarak eski haline döndürür.")
        else :
            print("böyle bir değer bulanamadı")