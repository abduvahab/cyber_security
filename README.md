# cyber_security

## spider

The spider program allow you to extract all the images from a website, recursively, by providing a url as a parameter. 

The program will download the following extensions by default:.jpg/jpeg,.png,.bmp


-usage
```sh
python spider.py [-rlpS] URL
• Option -r : recursively downloads the images in a URL received as a parameter.
• Option -r -l [N] : indicates the maximum depth level of the recursive download. If not indicated, it will be 5.
• Option -p [PATH] : indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.
```

## Scorpion

scorpion program receive image files as parameters and must be able to parse them for EXIF and other metadata, displaying them on the screen.

It display basic attributes such as the creation date, as well as EXIF data. The out-
put format is up to you.

usage
```sh

python scorpion.py FILE1 [FILE2 ...]
```


## ft_opt

the program  allows you to store an initial password in file, and that is capable of generating a new one time password every time it is requested.

 -g: The program receives as argument a hexadecimal key of at least 64 char- acters. The program stores this key safely in a file called ft_otp.key, which is encrypted.

 -k: The program generates a new temporary password based on the key given as argument and prints it on the standard output.

usage
```sh
python ft_opt.py -g path/64characters
python ft_opt.py -k ft_opt.key
```


<img width="629" alt="Screen Shot 2023-05-26 at 12 20 50 PM" src="https://github.com/abduvahab/cyber_security/assets/100579404/692dd59d-aa55-460e-8b13-2e0daf9fb691">




