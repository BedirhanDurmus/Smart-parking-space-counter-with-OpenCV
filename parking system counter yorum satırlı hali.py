import cv2  # OpenCV kütüphanesini içe aktarır
import pickle  # pickle kütüphanesini içe aktarır
import numpy as np  # numpy kütüphanesini içe aktarır

def checkParkSpace(imgg):  # Park alanını kontrol etmek için bir fonksiyon tanımlar
    spaceCounter = 0  # Boş park alanlarını saymak için bir sayaç başlatır
    
    for pos in posList:  # Pozisyon listesindeki her pozisyon için döngü başlatır
        x, y = pos  # Pozisyondaki x ve y koordinatlarını alır
        
        img_crop = imgg[y: y + height, x:x + width]  # Görüntüyü belirli bir pozisyonda kırpma
        count = cv2.countNonZero(img_crop)  # Kırpılmış görüntüdeki sıfır olmayan piksel sayısını hesaplama
        
        if count < 150:  # Eğer sıfır olmayan piksel sayısı 150'den az ise
            color = (0, 255, 0)  # Rengi yeşil yap
            spaceCounter += 1  # Boş park alanı sayısını artır
        else:  # Eğer sıfır olmayan piksel sayısı 150'den fazla ise
            color = (0, 0, 255)  # Rengi kırmızı yap
    
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, 2)  # Görüntü üzerine bir dikdörtgen çiz
        cv2.putText(img, str(count), (x, y + height - 2), cv2.FONT_HERSHEY_PLAIN, 1,color,1)  # Görüntü üzerine piksel sayısını yaz
    
    cv2.putText(img, f"Free: {spaceCounter}/{len(posList)}", (15,24), cv2.FONT_HERSHEY_PLAIN, 2,(0,255,255),4)  # Görüntü üzerine boş park alanı sayısını yaz

width = 27  # Kırpılacak görüntünün genişliğini belirler
height = 15  # Kırpılacak görüntünün yüksekliğini belirler

cap = cv2.VideoCapture("video.mp4")  # Videoyu okumak için bir VideoCapture nesnesi oluşturur

with open("CarParkPos", "rb") as f:  # Dosyayı okuma modunda açar
    posList = pickle.load(f)  # Dosyadan pozisyon listesini yükler

while True:  # Sonsuz bir döngü başlatır
    success, img = cap.read()  # Videodan bir kare okur
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Görüntüyü griye dönüştürür
    imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)  # Görüntüyü bulanıklaştırır
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)  # Görüntüyü ikili hale getirir
    imgMedian = cv2.medianBlur(imgThreshold, 5)  # Görüntüyü median blur filtresi ile düzeltir
    imgDilate = cv2.dilate(imgMedian, np.ones((3,3)), iterations = 1)  # Görüntüyü genişletir
    
    checkParkSpace(imgDilate)  # Park alanını kontrol eder
    
    cv2.imshow("img", img)  # Görüntüyü gösterir
    cv2.waitKey(200)  # Belirli bir süre bekler
Bu kod, bir video üzerindeki park alanlarını kontrol eder ve her bir park alanının durumunu (boş veya dolu) gösterir. Ayrıca, boş park alanlarının sayısını da gösterir. Bu, bir otopark yönetim sistemi için kullanışlı olabilir. Kod, OpenCV, pickle ve numpy kütüphanelerini kullanır. Bu kütüphaneler, görüntü işleme ve veri manipülasyonu için güçlü araçlar sağlar. Kodun genel amacı, bir video akışından park alanlarının durumunu tespit etmektir. Bu, bir otoparkta boş yerlerin otomatik olarak tespit edilmesi için kullanılabilir. Bu tür bir sistem, özellikle büyük otoparklarda, kullanıcıların boş yerleri daha hızlı bulmasına yardımcı olabilir. Bu, hem kullanıcı deneyimini iyileştirir hem de otoparkın genel verimliliğini artırır. Bu kod, bu tür bir sistemin temel bir parçası olabilir. Ancak, bu kodun tam bir otopark yönetim sistemi oluşturmak için daha fazla özellik ve işlevsellik eklenmesi gerektiğini unutmayın