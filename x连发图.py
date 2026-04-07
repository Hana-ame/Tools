from pynput.keyboard import Key, Controller
import time

# 创建键盘控制器
keyboard = Controller()

short = 0.5
long = 3

l=[
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433415apy542wuncz.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433416gcugvanc4pt.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433417ekhrsybjva0.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433418n0ly5p3hkao.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433419l32auy2pgbe.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433420vx5ftaykuyo.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433421ckaw1edxcqg.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433422ca3xtlbhtwn.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433423f4kztdiu3aj.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433424oiyln3rt2ba.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433425o02k3jjlgr1.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433426r40gp32mfyu.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433427nterxgu2n4n.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433428rftokpocz5m.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/4334290u5jzyitgkp.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/4334303ft0zadeggr.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433431ljkv2uxigjr.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433432noi4ji50jkx.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433433vc0trcfpgum.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433434iblqgmk44ae.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433435nhyq5kzldev.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433436cp3ggwvcru3.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433437jueuxtjbigu.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/4334380khyi0ch4li.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433439yt4vu0ttofq.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433440ac2cfeixq1g.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433441fey33hudgou.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433442olbfh0yesrt.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433443grmde321uz3.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433444fxiaxmn0axk.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433445i3m4qvdy0st.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433446xxb25aiop3v.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433447cnkts0evcut.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433448o1dhlhcklhn.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433449tuq4oidlvhr.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/4334503rqzjc4hr1u.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433451swrtl3oct1x.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433452idt1bz14ukd.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433453unjw4fxpii3.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433454ilt3pfhqrw3.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433455rkkj4zxhxbh.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433456czpr0q0nbfv.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/4334571vmg0i1wpai.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433458ptp4gz1xfc1.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433459bfddraffpyf.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433460xdkhsd3rb4f.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433461304xkdvm1ug.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433462hrr5yspgowi.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433463gifpgmk4dpt.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/43346445vbb351yol.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433465lz0l3cotray.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433466l4gcklh40tb.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433467oo4p4mbneow.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433468aykf0bgjgl5.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/4334692tjfg52syut.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433470yxjmwxwdpkm.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433471cx3ffqwvkrk.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433472lsvtbp0sp31.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/4334733evuu5tgvcx.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433474mo4uxxs4q0u.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433475ve41u2xhaet.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433476qjbdpvidvgv.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433477fq1rasdbepc.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/43347855loxvlgmvl.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/4334792eqeihl0dv3.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433480hrdibfa2lvu.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433481wd0h0jziuxw.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433482m1f1f2wxhav.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433483hf21t5uskgs.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433484wc4cjmwelil.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433485z4cuio5pe5k.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/4334861gm4lu3a3wo.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433487lpjm5idrzgx.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433488pzl2l1llo4c.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433489rpdfepchrla.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/4334905jj1ympk5o4.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433491pxxjubt4rlw.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433492dcfkq0znw2s.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433493dozdrnv4t1u.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433494eenmvlyx5ne.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433495gg0dzvlfzcj.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/4334963vzp1c2gne1.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433497cnbpydo05q2.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433498zs5tkpmgonz.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433499leqqbamhqaa.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433500gwezdx21nvz.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433501xiow5pbvxws.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/4335021ubg0igsqvf.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433503ldwxc00rmmg.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433504jldenfgp1kd.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433505ace0fkldahp.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433506d1qxx5ijhsn.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433507eitzql3f2cq.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433508k0lromjrfjj.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433509xpv45h1xsre.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433510fefnyyp15fy.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433511dp0a3l2j0gl.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433512oxpt4lm2yai.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/4335130tg4lxgi0ep.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/4335140yn3n2wfvch.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433515zdnyrcqlea5.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433516yaay3jwtbi3.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433517s4u4b4ijepi.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/43351842x0zcqudwy.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433519wtdnp0jy2qw.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/4335203pfzudumx5v.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433521viqpbdylgrt.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433522ixh4tr1r1vq.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433523rdcrvv0ptoe.jpg",
    "/static/images/2023/04/15/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202020-04-09/433524jq1i1iech4d.jpg",

    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37642vmqjxwf32l4.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37643f24iapfqygz.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37644kehcfrdajm5.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37645lhdnfvrd3il.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37646qgrkhg1rzat.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37647mni2xwvpc5z.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/376481wwc3gtyhmv.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37649522lsyn1y3k.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37650v33ilb5mzl3.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37651pla2kfar52d.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/376520pzjpl1qzn0.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/376533jnicvxbvvg.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/376543ae0pcubfkz.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37655qvqovxcu2dn.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37656vir2b1lqhbv.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37657kdqghdy0lii.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37658esy0xectzvy.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37659vweci1u1i3w.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37660puwdwf0454s.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37661rfn04ndkmn3.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37662rofls2r2rjs.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37663s21yhzproe0.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37664iilymaujdtf.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37665pwn2cs3ymdu.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/3766645lao3txuox.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37667pacnkxoiffk.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37668ayzlcnyvvmg.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37669mcrqale3i40.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37670w0wy1mofnxp.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/376710awoir3cl3y.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/376720v0ylifbutk.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37673fwrdl0rv4to.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37674oglcgxovvig.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37675pcvb1gnrrk5.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37676pseu3ozi02k.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37677c4x43weyzrb.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37678pmj4fr52np1.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/376793raurkbesvg.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37680skvof3q3adh.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37681bga2vj35mvl.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/3768241cnz3djpsw.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37683sqm5h4aezn3.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37684x3tp0xcvvaf.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/3768500miloko33c.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37686rltss2tlrop.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37687fjfreq2rrmh.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37688j1oj4dssdkj.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37689gryzobf0jgb.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/3769003lzx4snjab.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/376911ck0ene2pj4.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37692nsayz2hurc1.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37693iklgkrlxkcl.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37694hbpi4vensah.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37695lgfu1xshdrz.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37696h30gibhqudt.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37697nfzc1aupj03.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37698cixswhwofvb.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37699rs0lv4yqpbi.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/377000z0qozi1vkv.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37701qlaa553zo10.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37702zetw4dm55ar.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37703jdu0gw4f0vb.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37704xr21xmdrzf4.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37705wdkgsycprwu.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37706ezmskrtnkel.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37707vpihhomyvyi.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/377081a0magib332.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/377095sqixibofcc.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37710xabsehhb40m.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/377111iwdiplbsvj.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37712jtqh3r2p2a2.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37713od1tcqqji0p.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37714n1ydflck2su.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37715kuhvks3iirr.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37716awdscdvelx1.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37717kc2jy4jv20u.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/3771844dad3dxjiw.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37719epn5zrobwar.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37720ix0grg2dilh.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37721qqgtfx3mwqo.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37722ic31ndtol0f.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37723p0nj13apy4g.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37724ojlkp40p0x5.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37725t1ucmdkffno.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37726mgntrsmed5f.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37727bf2md3pyltu.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37728objhm1ca0ho.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/3772953yhtlkvf0l.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/377300g51odqd23n.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37731fzz1alev1yv.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37732jmhjkxgmvkt.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37733agxzck4qigx.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37734hnc12cbskh1.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/377353rygsvs3ayf.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37736gzzchrmbtj2.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37737ojdzaffww4f.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37738m1rr5oa1z50.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37739donbuvyaq3x.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37740rvmxfvbw41r.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37741b0beftxbrjd.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37742vsbz2mfuhqs.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37743vqpbvpbbsow.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37744xalctidznff.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37745exu2r2oyd1u.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37746ishs1odlqgn.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37747qn3narlcuve.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37748vfvtxfver4p.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37749s0bnvdiokil.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37750simsgfx3hj3.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37751pkqe4uouox2.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37752ym3caioc1kg.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37753c40ik4kd35j.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/377541thxk02k4qs.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/3775542lpy13pzws.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/377560molcixu2ot.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37757v0lv3vbufkp.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/377580gmnquzbkep.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37759l1frxan513z.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37760mu5zwix4fnj.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37761anm41xq4zcc.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37762ksnv0jghhva.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37763nj5f5kdkjyg.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37764nzpcqluqzag.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37765r03hp2a0l5r.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37766f45mzevxact.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/377671sifvzx3cv2.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37768i51lev4n25z.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37769zi5kxbk4mc4.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37770rak3idmpxes.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/377711tliqxj2ipj.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37772kddmo0ub1e5.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37773biakgxt4k1a.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37774ebs2f51pgkk.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/377750l4ibm10myu.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37776dtmz40zuv4i.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37777fog31tlmoep.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37778o21qpyfyusp.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/377792onqa4orpkz.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37780u0yrvwehqeq.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37781ybr1mz0skjj.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37782u25fjunojnc.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/377832pdkh4gxvzp.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/377841340e2ylnew.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37785wnbxidnhd5w.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37786jyz42vhaa25.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37787uvhd2o4comz.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37788luckfd5wawa.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37789dx5ekt3x52z.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37790zo1e5m3diwq.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37791asydhiogstn.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37792o1s4ncftart.jpg",
    "/static/images/2023/05/08/%E8%A5%BF%E7%93%9C%E5%B0%91%E5%A5%B3%20-%202021-05-15/37793qax1rvik3hn.jpg"
]


def simulate_operations(n):
    """
    模拟执行指定次数的操作序列
    1. Win+V
    2. 下箭头n次
    3. Enter
    4. Enter
    """
    # 给用户时间切换到目标窗口
    print("程序将在3秒后开始，请确保切换到目标窗口...")
    time.sleep(3)

    # 循环执行操作
    for i in range(n - 1, 0 - 1, -1):
        print(f"执行第 {n-i} 次循环")

        # 1. 按下 Win+V
        keyboard.press(Key.cmd)
        keyboard.tap("v")
        keyboard.release(Key.cmd)
        time.sleep(short)  # 等待剪贴板打开

        # 2. 按下箭头n次
        for _ in range(i):  # 当前循环按下对应次数
            keyboard.tap(Key.down)
            time.sleep(short)

        # 3. 第一次按 Enter
        keyboard.tap(Key.enter)
        time.sleep(short)
        keyboard.tap(Key.enter)

        time.sleep(long)

    print(f"操作完成，最终 n = {n}")


def from_list():
    """
    模拟执行指定次数的操作序列
    1. Win+V
    2. 下箭头n次
    3. Enter
    4. Enter
    """
    # 给用户时间切换到目标窗口
    print("程序将在3秒后开始，请确保切换到目标窗口...")
    time.sleep(3)

    # 循环执行操作
    for i in range(len(l)):
        print(f"执行第 {i+1} 次循环")

        keyboard.type("https://xx.knit.bid")
        keyboard.type(l[i])

        keyboard.tap(Key.enter)

        time.sleep(long)

    print(f"操作完成，最终 n = {n}")

    pass


if __name__ == "__main__":
    try:
        # 获取用户输入的循环次数
        n = int(input("请输入循环次数 n: "))

        if n <= 0:
            print("循环次数必须大于0")
        else:
            simulate_operations(n)

    except ValueError:
        from_list()
    except Exception as e:
        print(f"程序执行出错: {e}")
