import tkinter as tk

HEIGHT = 700
WIDTH = 800

def bringToFront(frame):
    frame.tkraise()

root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg='#99ceff')
canvas.pack()

loginFrame = tk.Frame(root, bg ='#99ceff')
loginFrame.place(relwidth = .5, relheight = .5, relx = .24, rely = .15)

loginButton = tk.Button(loginFrame, text="Log In", bg='gray')
loginButton.place(relx = .45, rely = .52)

usernameLabel = tk.Label(loginFrame, text='Username: ', bg='#99ceff')
usernameLabel.place(relx = .19, rely = .4)

usernameEntry = tk.Entry(loginFrame, bg='gray')
usernameEntry.place(relx = .36, rely = .4)

passwordLabel = tk.Label(loginFrame, text='Password: ', bg='#99ceff')
passwordLabel.place(relx = .19, rely = .45)

passwordEntry = tk.Entry(loginFrame, bg='gray')
passwordEntry.place(relx = .36, rely = .45)

noAccountLabel = tk.Label(loginFrame, text="Don't have an account?", bg='#99ceff')
noAccountLabel.place(relx = .35, rely = .75)

signUpButton = tk.Button(loginFrame, text="Sign Up!", bg='gray', command=lambda:bringToFront(signUpFrame))
signUpButton.place(relx = .435, rely = .83)



signUpFrame = tk.Frame(root, bg='#99ceff')
signUpFrame.place(relheight = 1, relwidth = 1)

signUpScreenSignUpButton = tk.Button(signUpFrame, text="Sign Up", bg='gray')
signUpScreenSignUpButton.place(relx = .455, rely = .52)


signUpUsernameLabel = tk.Label(signUpFrame, text='Username: ', bg='#99ceff')
signUpUsernameLabel.place(relx = .25, rely = .35)

signUpUsernameEntry = tk.Entry(signUpFrame, bg='gray')
signUpUsernameEntry.place(relx = .41, rely = .35)


signUpEmailLabel = tk.Label(signUpFrame, text='Email: ', bg='#99ceff')
signUpEmailLabel.place(relx = .25, rely = .40)

signUpEmailEntry = tk.Entry(signUpFrame, bg='gray')
signUpEmailEntry.place(relx = .41, rely = .40)


signUpPasswordLabel = tk.Label(signUpFrame, text='Password: ', bg='#99ceff')
signUpPasswordLabel.place(relx = .25, rely = .45)

signUpPasswordEntry = tk.Entry(signUpFrame, bg='gray')
signUpPasswordEntry.place(relx = .41, rely = .45)

signUpReturnToLoginButton = tk.Button(signUpFrame, bg='gray', text='Return to Login Screen', command=lambda:bringToFront(loginFrame))
signUpReturnToLoginButton.place(relx = .41, rely = .6)



loginFailedFrame = tk.Frame(root, bg = '#99ceff')
loginFailedFrame.place(relheight = 1, relwidth = 1)

loginFailedLabel = tk.Label(loginFailedFrame, text='Login failed. Username and Password not recognized.',  bg='#99ceff')
loginFailedLabel.place(relx = .33, rely = .4)

returnToLoginButton = tk.Button(loginFailedFrame, text='Return to Login Screen', bg='grey', command=lambda:bringToFront(loginFrame))
returnToLoginButton.place(relx = .42, rely = .5)

bringToFront(loginFailedLabel)
root.mainloop()

