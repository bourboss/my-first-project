from celestial_body import Body
from simulator import Simulator

earth = Body(6e24,0,29783,1.5e11,0)
sun = Body(2e30,0,0,0,0)

test = Simulator([earth, sun],3600)
for i in range(8760):
    test.step()
    if i % 1000 == 0:
        print(f"Step {i}: Earth at ({earth.p_x:.3e}, {earth.p_y:.3e})")