from flask_bcrypt import Bcrypt

pass_hash = Bcrypt().generate_password_hash('12345')
print(pass_hash)

check_pass = Bcrypt().check_password_hash(pass_hash, '123456')
print(check_pass)