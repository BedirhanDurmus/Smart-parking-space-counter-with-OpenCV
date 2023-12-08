import cv2  # OpenCV kütüphanesini içe aktarır, görüntü işleme için kullanılır
import pickle  # pickle modülünü içe aktarır, Python nesnelerini dosyalara kaydetmek ve yüklemek için kullanılır

width = 27  # Genişlik değerini belirler
height = 15  # Yükseklik değerini belirler

try:  # Aşağıdaki kod bloğunu dener
    with open("CarParkPos", "rb") as f:  # "CarParkPos" adlı dosyayı okuma modunda açar
        posList = pickle.load(f)  # Dosyadan Python nesnesini yükler
except:  # Yukarıdaki kod bloğunda hata oluşursa
    posList = []  # posList'i boş bir liste olarak başlatır

def mouseClick(events, x, y, flags, params):  # Fare tıklama olaylarını işleyen bir fonksiyon tanımlar
    
    if events == cv2.EVENT_LBUTTONDOWN:  # Eğer sol fare tuşuna basılırsa
        posList.append((x, y))  # Tıklanan konumu listeye ekler
    
    if events == cv2.EVENT_RBUTTONDOWN:  # Eğer sağ fare tuşuna basılırsa
        for i, pos in enumerate(posList):  # Listede her pozisyon için
            x1, y1 = pos  # Pozisyon koordinatlarını alır
            if x1 < x < x1 + width and y1 < y < y1 + height:  # Eğer tıklanan konum belirli bir alanın içindeyse
                posList.pop(i)  # Bu pozisyonu listeden çıkarır
    with open("CarParkPos","wb") as f:  # "CarParkPos" adlı dosyayı yazma modunda açar
        pickle.dump(posList, f)  # Python nesnesini dosyaya yazar

while True:  # Sonsuz bir döngü başlatır
    img = cv2.imread("first_frame.png")  # Bir görüntü dosyasını okur
    
    for pos in posList:  # Listede her pozisyon için
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255,0,0),2)  # Görüntü üzerine bir dikdörtgen çizer
    # print("poslist: ",posList)  # Pozisyon listesini yazdırır
    
    cv2.imshow("img", img)  # Görüntüyü gösterir
    cv2.setMouseCallback("img", mouseClick)  # Fare olaylarını işlemek için bir geri çağırma fonksiyonu belirler
    cv2.waitKey(1)  # Belirli bir süre boyunca bir tuşa basılmasını bekler
Bu kod, bir görüntü üzerinde fare tıklamalarıyla belirli konumlara dikdörtgenler çizmeye ve bu dikdörtgenleri kaldırmaya yarar. Bu dikdörtgenlerin konumları, bir dosyada saklanır ve program her başladığında bu dosyadan yüklenir. Bu, belirli konumların kalıcı olarak saklanmasını sağlar. Bu kod genellikle, bir görüntü üzerinde belirli konumları işaretlemek için kullanılır. Örneğin, bir otopark görüntüsünde park yerlerini işaretlemek için kullanılabilir.