from malange import Malange

f = open("hello-world.mala", "r")

m = Malange()

m.loadFile(f.read())

f.close()
