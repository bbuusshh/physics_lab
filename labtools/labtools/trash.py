# from scipy.optimize import minimize
# sys_args.update(pulse_args)
# def miniDip(vals):
#   sys_tot = dict(zip(list(array['name']),list(vals)))
#   tlist, res = evolve(sys_tot, pulse_func=pulse_with_bg)
#   range_p=(tlist<125)*(tlist>70)
#   return np.min(res.expect[0][range_p]/res.expect[0][range_p][0])
# array = np.array(list(sys_args.items()), dtype=[('name', '<U10'), ('value', 'int')])
# popt = minimize(miniDip, array['value'], bounds=((0.5, 3), (0, 0.01), (0.08, 0.12), (0.1, 4.15), (0.4, 2), (80, 90), (0.1, 0.3)))
# popt.x
# sys_opt = dict(zip(list(array['name']),list(popt.x)))
# tlist, result = evolve(sys_opt, pulse_func=pulse_with_bg)
# range_p=(tlist<165)*(tlist>70)
# plt.plot(tlist[range_p], result.expect[0][range_p])
# plt.ylim(0)
# plt.plot(tlist[range_p], result.expect[1][range_p])