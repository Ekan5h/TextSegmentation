def Otsu(hist):
    thresh = 0
    maxvar = 0
    P1 = 0
    P2 = 1
    m1 = 0
    m2 = sum([i*hist[i] for i in range(256)])
    var = 0
    for i in range(256):
        if(P1!=0 and P2!=0):
            var = P1*P2*((m1/P1-m2/P2)**2)
        P1 += hist[i]
        P2 -= hist[i]
        m1 += i*hist[i]
        m2 -= i*hist[i]
        if(var>maxvar):
            thresh = i
            maxvar = var
    return thresh

def dfs(img, i, j, mx, Mx, my, My):
    mx = min(mx, i)
    Mx = max(Mx, i)
    my = min(my, j)
    My = max(My, j)
    img[i][j] = 0
    if(i+1<img.shape[0] and img[i+1][j]>0.5):
        m = dfs(img, i+1, j, mx, Mx, my, My)
        mx = min(mx, m[0])
        Mx = max(Mx, m[1])
        my = min(my, m[2])
        My = max(My, m[3])
    if(i>0 and img[i-1][j]>0.5):
        m = dfs(img, i-1, j, mx, Mx, my, My)
        mx = min(mx, m[0])
        Mx = max(Mx, m[1])
        my = min(my, m[2])
        My = max(My, m[3])
    if(j+1<img.shape[1] and img[i][j+1]>0.5):
        m = dfs(img, i, j+1, mx, Mx, my, My)
        mx = min(mx, m[0])
        Mx = max(Mx, m[1])
        my = min(my, m[2])
        My = max(My, m[3])
    if(j>0 and img[i][j-1]>0.5):
        m = dfs(img, i, j-1, mx, Mx, my, My)
        mx = min(mx, m[0])
        Mx = max(Mx, m[1])
        my = min(my, m[2])
        My = max(My, m[3])
    return [mx, Mx, my, My]
