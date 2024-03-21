import cv2
import img as i



def main():
    img = i.Image()
    objects,biggest= img.compare()
    cv2.imshow("all", objects)
    cv2.imshow("biggest", biggest)

    cv2.imwrite('all.png',objects)
    cv2.imwrite('biggest.png',biggest)


    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()