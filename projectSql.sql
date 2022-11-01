--create database proje_final
/*
create table destekleyenler(
sirket_no int identity (1,1) not null primary key,
sirket_ismi varchar(20),
ülke varchar(10),
)
*/
/*
create table kullanýcýlar(
kullanýcýId int identity (1,1) not null primary key,
kullanýcýAd varchar(20),
ismi varchar(20),
soyismi varchar(20),
telNo varchar(20)
)
*/
/*
create table gelisitiriciler(
gelisitiriciNo int identity (1,1) not null primary key,
topluluk_ismi varchar(50),
ülke varchar(20),
bilgi varchar(300)
)
*/
/*
create table algoritma_türleri(
algoritma_kodu varchar(20) not null primary key,
byte_uzunluk int,
gelisitiriciNo int,
foreign key(gelisitiriciNo) references gelisitiriciler(gelisitiriciNo),
cikis_tarihi date
)
*/
/*
create table kodlama_dilleri(
dil_Kodu varchar(10) not null primary key,
dil_adý varchar(20),
cikis_tarihi date,
sirket_no int,
foreign key(sirket_no) references destekleyenler(sirket_no)
)
*/
/*
create table sifrelenmis_metin(
sifrelenen_metinID int identity(1,1) not null primary key,
sifrelenen_metin varchar(300),
algoritma_kodu varchar(20),
foreign key(algoritma_kodu) references algoritma_türleri(algoritma_kodu),
dil_Kodu varchar(10),
foreign key(dil_Kodu) references kodlama_dilleri(dil_Kodu),
kullanýcýId int,
foreign key(kullanýcýId) references kullanýcýlar(kullanýcýId),
)
*/

/*
insert into kullanýcýlar values('zet','emre','topal','05511569874')
insert into kullanýcýlar values('bntunc','bunyamin','tünç','05511568545')
insert into kullanýcýlar values('tlhamrlc','talha','marulcu','05526984521')
insert into kullanýcýlar values('erykrtloglu','eray','kartaloðlu','05589523698')
insert into kullanýcýlar values('slmbrke','selim','ilban','05511545558')
*/
--insert into destekleyenler values('microsoft','amerika')
--insert into destekleyenler values('Python Yazýlým Vakfý','amerika')
--insert into destekleyenler values('oracle','amerika')
--insert into destekleyenler values('Mozilla Foundation','amerika')
--insert into destekleyenler values('Google','amerika')

--insert into gelisitiriciler values('Ulusal Güvenlik Ajansý','amerika','SHA-2, ABD Ulusal Güvenlik Ajansý tarafýndan tasarlanmýþ kriptografik özet fonksiyonlarý kümesidir. Kriptografik özet fonksiyonlarý, hesaplanmýþ “özet” ile bilinen ve beklenen özet deðerinin karþýlaþtýrýlmasýyla, dijital veri üzerinde yürüyen matematiksel operasyonlardýr.')
--insert into gelisitiriciler values('Ron Rivest','amerika','Ronald Linn Rivest, Amerikalý þifrebilimci. Massachusetts Teknoloji Enstitüsünde profesör olarak görev yapmaktadýr.')
--insert into gelisitiriciler values('Dan Bernstein','amerika','Daniel Julius Bernstein, Amerikalý bir Alman matematikçi, kriptolog ve bilgisayar bilimcisidir. Bochum Ruhr Üniversitesinde CASAda misafir profesör ve Chicagodaki Illinois Üniversitesinde Bilgisayar Bilimleri Araþtýrma Profesörüdür.')

/*
insert into kodlama_dilleri values('py','python','1990-10-10',2)
insert into kodlama_dilleri values('c#','c sharp','2000-05-11',1)
insert into kodlama_dilleri values('js','javascript','1995-10-10',6)
insert into kodlama_dilleri values('drt','dart','2013-12-12',5)
insert into kodlama_dilleri values('jv','java','1995-08-08',3)
*/

/*
insert into algoritma_türleri values('sha-256',32,1,'2004-10-10')
insert into algoritma_türleri values('sha-512',32,1,'2008-10-10')
insert into algoritma_türleri values('sha-224',32,1,'2008-10-10')
insert into algoritma_türleri values('md-5',128,2,'2007-10-10')
insert into algoritma_türleri values('blank2b',64,3,'2009-06-09')
insert into algoritma_türleri values('blank2s',64,3,'2009-06-09')
insert into algoritma_türleri values('rsa',32,2,'2007-06-09')
insert into algoritma_türleri values('ferned',64,3,'2010-06-09')
*/
--CASCADING
/*
ALTER TABLE sifrelenmis_metin  WITH CHECK ADD  CONSTRAINT [Fk_cons] FOREIGN KEY([kullanýcýId])
REFERENCES kullanýcýlar ([kullanýcýId])
ON DELETE NO ACTION
GO
*/

/*
ALTER TABLE sifrelenmis_metin  WITH CHECK ADD  CONSTRAINT [Fk_cons2] FOREIGN KEY([algoritma_kodu])
REFERENCES algoritma_türleri ([algoritma_kodu])
ON DELETE NO ACTION
GO
*/

/*
ALTER TABLE sifrelenmis_metin  WITH CHECK ADD  CONSTRAINT [Fk_cons3] FOREIGN KEY([dil_Kodu])
REFERENCES kodlama_dilleri ([dil_Kodu])
ON DELETE NO ACTION
*/

--CONSTRAINTLER
/*
alter table algoritma_türleri add constraint CN_algoritmakodu
unique (algoritma_kodu)
*/

/*
alter table kodlama_dilleri add constraint CN_dil_Kodu
unique (dil_Kodu)
*/

 /*
alter table sifrelenmis_metin add constraint DF_dil_Kodu
default 'py' for dil_Kodu
*/

/*
alter table sifrelenmis_metin add constraint CN_sifrelenen_metin_len
check (len(sifrelenen_metin)>5)
*/

/*
alter table kodlama_dilleri add constraint CN_cikis_tarihi
check (cikis_tarihi<getdate())
*/

--RULES
--create rule rl_uzunluk as len(@value)<=10
--exec sp_bindrule rl_uzunluk,'kodlama_dilleri.dil_Kodu'

--create rule rl_tarih as @value<getdate()
--exec sp_bindrule rl_tarih,'algoritma_türleri.cikis_tarihi'


--STORED PROCEDURE

--kullanýcýID si xxx olan kullanýcýnýn yaptýðý hash islemlerini gösteren store procedure
/*
create procedure kullanýcý_arama
(@kullanýcýId int)
as
select * from sifrelenmis_metin s inner join kullanýcýlar k on s.kullanýcýId=k.kullanýcýId where k.kullanýcýId=@kullanýcýId
*/
--exec kullanýcý_arama 1

/*
create procedure algoritma_arama
(@AlgoritmaKodu varchar(10))
as
select * from sifrelenmis_metin s join algoritma_türleri a on s.algoritma_kodu=a.algoritma_kodu
where a.algoritma_kodu=@AlgoritmaKodu
*/
--exec algoritma_arama 'sha-256'

--VIEW

--python ile yazýlan kodlarýn þifrelenen metinlerini gösteren tablo
/*
create view py_yazýlan
as
select sifrelenen_metin from sifrelenmis_metin s where s.dil_Kodu='py'
*/
--select * from py_yazýlan

--çýkýþ tarihi 2000 öncesi olan kodlama dillerini listeleyen tablo
/*
create view cikis_tarih
as
select * from kodlama_dilleri where year(cikis_tarihi)<2000 
*/
--select * from cikis_tarih

--büyüklüðü 32 byte üstü olan algoritma türlerini listeleyen tablo
/*
create view byte_uzunluk
as
select * from algoritma_türleri where byte_uzunluk>32
*/
--select * from byte_uzunluk

--TABLO DÖNDÜREN FONKSÝYON

--kodlama dillerini destekleyen þirketlerin ülkelerine göre arama yapan fonksiyon
/*
create function search_ulke(@ulke_ismi varchar(20))
returns table
as
return select * from destekleyenler where ülke=@ulke_ismi
*/
--select * from search_ulke('amerika')


--þifreleme algoritmalarýnýn geliþtiricilerini yazdýran fonksiyon
/*
create function gelistirici_isim()
returns table
as
return select a.algoritma_kodu,g.topluluk_ismi from gelisitiriciler g inner join algoritma_türleri a on g.gelisitiriciNo=a.gelisitiriciNo  
*/
--select * from gelistirici_isim()

--KULLANICI TANIMLI FONKSÝYON 

--x kodlama dili ile yazýlan þifreleme algoritmalarýnýn türlerinin büyüklüðünün ortalamasýný alan fonksiyon
/*
create function ortalama_buyukluk(@kod_dili varchar(10))
   returns int
   as
   begin 
     declare @ortalama int
	 select @ortalama=avg(byte_uzunluk) from algoritma_türleri a join sifrelenmis_metin s on a.algoritma_kodu=s.algoritma_kodu 
	 where s.dil_Kodu=@kod_dili
	 return @ortalama
   end
   */
--select dbo.ortalama_buyukluk('py') as 'byte ortalamasý'


--kodlama dillerinin kaç yýllýk olduðunu bulan 
/*
create function kac_yýllýk(@dil_kdu varchar(10))
returns int
as
begin
declare @yil int
select @yil=year(getdate())-year(cikis_tarihi) from kodlama_dilleri where dil_Kodu=@dil_kdu
return @yil
end
*/
--select dbo.kac_yýllýk('jv') as 'yas'
 
--TRIGGER

/*
create trigger ekleme
on kullanýcýlar
after insert 
as 
begin 
       select 'yeni kullanýcý eklendi'
end
*/
--insert into kullanýcýlar values('hasnkya','hasan','kaya','05516984525')