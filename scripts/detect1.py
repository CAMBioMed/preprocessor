# python
import cv2
import numpy as np
import math

def white_balance(img):
    # simple gray\-world white balance (scale each channel to common mean)
    b, g, r = cv2.split(img.astype(np.float32))
    mb, mg, mr = b.mean(), g.mean(), r.mean()
    m = (mb + mg + mr) / 3.0
    b = np.clip(b * (m / mb), 0, 255)
    g = np.clip(g * (m / mg), 0, 255)
    r = np.clip(r * (m / mr), 0, 255)
    return cv2.merge([b, g, r]).astype(np.uint8)

def make_mask(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    # white: low saturation, high value
    mask_white = cv2.inRange(hsv, (0, 0, 120), (180, 60, 255))
    # also include bright colored tape (saturated & bright) to avoid holes
    mask_color = cv2.inRange(hsv, (0, 80, 120), (180, 255, 255))
    mask = cv2.bitwise_or(mask_white, mask_color)
    # morphological cleanup
    kern = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kern, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kern, iterations=1)
    return mask

def length_of_line(l):
    x1,y1,x2,y2 = l
    return math.hypot(x2-x1, y2-y1)

def line_angle_deg(l):
    x1,y1,x2,y2 = l
    ang = math.degrees(math.atan2((y2-y1),(x2-x1)))
    if ang < 0: ang += 180
    return ang

def intersection(l1, l2):
    # line in form (x1,y1,x2,y2)
    x1,y1,x2,y2 = l1
    x3,y3,x4,y4 = l2
    denom = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if abs(denom) < 1e-6:
        return None
    px = ((x1*y2 - y1*x2)*(x3-x4) - (x1-x2)*(x3*y4 - y3*x4))/denom
    py = ((x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4 - y3*x4))/denom
    return (int(px), int(py))

def try_hough(mask, orig_img):
    edges = cv2.Canny(mask, 50, 150)
    linesP = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=80, minLineLength=100, maxLineGap=40)
    if linesP is None:
        return None
    lines = [l[0] for l in linesP]
    # separate near\-horizontal and near\-vertical
    horiz = []
    vert = []
    for l in lines:
        ang = line_angle_deg(l)
        if ang < 30 or ang > 150:
            horiz.append((length_of_line(l), l))
        elif 60 < ang < 120:
            vert.append((length_of_line(l), l))
    if len(horiz) < 2 or len(vert) < 2:
        return None
    horiz.sort(reverse=True); vert.sort(reverse=True)
    # pick top 2 of each
    top_h = [horiz[i][1] for i in range(min(2, len(horiz)))]
    top_v = [vert[i][1] for i in range(min(2, len(vert)))]
    # compute 4 intersections
    corners = []
    for h in top_h:
        for v in top_v:
            pt = intersection(h, v)
            if pt is not None:
                corners.append(pt)
    if len(corners) < 4:
        return None
    # choose 4 corners by convex hull / contour to order them
    pts = np.array(corners, dtype=np.int32)
    hull = cv2.convexHull(pts)
    if len(hull) < 4:
        return None
    hull = hull.squeeze()
    # if hull has more than 4 pts, approximate
    approx = cv2.approxPolyDP(hull, epsilon=10, closed=True)
    if len(approx) == 4:
        quad = approx.reshape(4,2)
    else:
        # fallback: take 4 extreme points (tl,tr,br,bl)
        xs = pts[:,0]; ys = pts[:,1]
        s = xs + ys; d = xs - ys
        tl = pts[np.argmin(s)]; br = pts[np.argmax(s)]
        tr = pts[np.argmin(d)]; bl = pts[np.argmax(d)]
        quad = np.array([tl, tr, br, bl])
    return quad

def fallback_contour(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours: return None
    c = max(contours, key=cv2.contourArea)
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02*peri, True)
    if len(approx) == 4:
        quad = approx.reshape(4,2)
        return quad
    # if not quad, use minAreaRect
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect).astype(np.int32)
    return box

def order_quad(pts):
    # order points as tl,tr,br,bl
    rect = np.zeros((4,2), dtype="int")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1).reshape(-1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

if __name__ == "__main__":
    img = cv2.imread("./src/preprocessor/images/Kea5_3a-small.jpg")  # replace with your filename
    wb = white_balance(img)
    mask = make_mask(wb)
    quad = try_hough(mask, wb)
    if quad is None:
        quad = fallback_contour(mask)
    if quad is not None:
        quad = order_quad(np.array(quad))
        out = img.copy()
        cv2.polylines(out, [quad], isClosed=True, color=(0,255,0), thickness=4)
        for (x,y) in quad:
            cv2.circle(out, (x,y), 6, (0,0,255), -1)
        cv2.imwrite("pvc_detected.png", out)
        print("Saved pvc_detected.png with detected rectangle.")
    else:
        print("PVC frame not detected. Try tuning thresholds or parameters.")










