import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from seawater import eos80

# History of seabird25p.cfg file changes:

# [mccann@elvis i2MAP]$ pwd
# /mbari/M3/master/i2MAP
# [mccann@elvis i2MAP]$ ls -l */*/*/*/seabird25p.cfg
# -rwx------. 1        519 games  3050 Sep 20  2016 2017/01/20170117/2017.017.00/seabird25p.cfg
# -rwx------. 1        519 games  3050 Sep 20  2016 2017/01/20170117/2017.017.01/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3050 Sep 20  2016 2017/04/20170407/2017.097.00/seabird25p.cfg
# -rwx------. 1 robs       games  3050 Sep 20  2016 2017/05/20170508/2017.128.00/seabird25p.cfg
# -rwx------. 1 robs       games  3109 May 11  2017 2017/05/20170512/2017.132.00/seabird25p.cfg
# -rwx------. 1 robs       games  3109 May 11  2017 2017/06/20170622/2017.173.00/seabird25p.cfg
# -rwx------. 1        519 games  3109 May 11  2017 2017/08/20170824/2017.236.00/seabird25p.cfg
# -rwx------. 1        519 games  3109 May 11  2017 2017/09/20170914/2017.257.00/seabird25p.cfg
# -rwx------. 1 etrauschke games  3109 Jan 29  2018 2018/01/20180125/2018.025.00/seabird25p.cfg
# -rwx------. 1 henthorn   games  3109 Feb 15  2018 2018/02/20180214/2018.045.03/seabird25p.cfg
# -rwx------. 1 lonny      games  3667 Mar  2  2018 2018/03/20180306/2018.065.02/seabird25p.cfg
# -rwx------. 1 lonny      games  3667 Mar  2  2018 2018/04/20180404/2018.094.00/seabird25p.cfg
# -rwx------. 1 lonny      games  3667 Mar  2  2018 2018/06/20180618/2018.169.01/seabird25p.cfg
# -rwx------. 1 lonny      games  3667 Jul 19  2018 2018/07/20180718/2018.199.00/seabird25p.cfg
# -rwx------. 1 jana       games  3667 Aug 30  2018 2018/08/20180829/2018.241.01/seabird25p.cfg
# -rwx------. 1 lonny      games  3667 Oct 25  2018 2018/10/20181023/2018.296.00/seabird25p.cfg
# -rwx------. 1 jana       games  3667 Mar  2  2018 2018/12/20181203/2018.337.00/seabird25p.cfg
# -rwx------. 1 jana       games  3667 Mar  2  2018 2018/12/20181210/2018.344.01/seabird25p.cfg
# -rwx------. 1 jana       games  3667 Mar  2  2018 2018/12/20181210/2018.344.05/seabird25p.cfg
# -rwx------. 1 jana       games  3667 Mar  2  2018 2018/12/20181210/2018.344.06/seabird25p.cfg
# -rwx------. 1 jana       games  3667 Mar  2  2018 2018/12/20181210/2018.344.07/seabird25p.cfg
# -rwx------. 1 jana       games  3667 Mar  2  2018 2018/12/20181210/2018.344.08/seabird25p.cfg
# -rwx------. 1 jana       games  3667 Mar  2  2018 2018/12/20181210/2018.344.09/seabird25p.cfg
# -rwx------. 1 jana       games  3667 Mar  2  2018 2018/12/20181210/2018.344.10/seabird25p.cfg
# -rwx------. 1 jana       games  3667 Mar  2  2018 2018/12/20181210/2018.344.11/seabird25p.cfg
# -rwx------. 1 jana       games  3667 Mar  2  2018 2018/12/20181210/2018.344.12/seabird25p.cfg
# -rwx------. 1 jana       games  3667 Mar  2  2018 2018/12/20181210/2018.344.13/seabird25p.cfg
# -rwx------. 1 jana       games  3667 Mar  2  2018 2018/12/20181214/2018.348.00/seabird25p.cfg
# -rwx------. 1 jana       games  3667 Mar  2  2018 2018/12/20181214/2018.348.01/seabird25p.cfg
# -rwx------. 1 jana       games  3667 Mar  2  2018 2018/12/20181214/2018.348.02/seabird25p.cfg
# -rwx------. 1 jana       games  3667 Mar  2  2018 2018/12/20181214/2018.348.03/seabird25p.cfg
# -rwx------. 1 lonny      games  3667 Mar  2  2018 2019/01/20190107/2019.007.07/seabird25p.cfg
# -rwx------. 1 lonny      games  3667 Mar  2  2018 2019/01/20190107/2019.007.09/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2019/02/20190204/2019.035.10/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2019/02/20190226/2019.057.00/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2019/02/20190226/2019.057.01/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2019/02/20190226/2019.057.02/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2019/02/20190226/2019.057.03/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2019/02/20190226/2019.057.04/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2019/02/20190226/2019.057.05/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2019/02/20190226/2019.057.06/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2019/02/20190226/2019.057.07/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2019/02/20190226/2019.057.08/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2019/02/20190228/2019.059.01/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2019/04/20190408/2019.098.01/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2019/06/20190606/2019.157.00/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2019/06/20190606/2019.157.01/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2019/06/20190606/2019.157.02/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2019/07/20190709/2019.190.00/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2019/09/20190916/2019.259.01/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2019/10/20191007/2019.280.02/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2019/10/20191021/2019.294.00/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2019/11/20191107/2019.311.00/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2019/12/20191210/2019.344.06/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2020/01/20200108/2020.008.00/seabird25p.cfg
# -rwx------. 1 mbassett   nobody 3667 Mar  2  2018 2020/02/20200210/2020.041.02/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2020/02/20200224/2020.055.01/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2020/06/20200629/2020.181.02/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2020/07/20200728/2020.210.03/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3667 Mar  2  2018 2020/08/20200811/2020.224.04/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3899 Sep 11  2020 2020/09/20200914/2020.258.01/seabird25p.cfg
# -rwx------. 1 lonny      nobody 3919 Sep 21  2020 2020/09/20200922/2020.266.01/seabird25p.cfg
# -rwxr-xr-x. 1 brian      games  4267 Mar  1  2021 2021/03/20210303/2021.062.01/seabird25p.cfg
# -rwxr-xr-x. 1 robs       games  4267 Mar  1  2021 2021/03/20210330/2021.089.00/seabird25p.cfg
# -rwxr-xr-x. 1 robs       games  4267 Mar  1  2021 2021/05/20210512/2021.132.01/seabird25p.cfg
# -rwxr-xr-x. 1 robs       games  4267 Mar  1  2021 2021/06/20210624/2021.175.03/seabird25p.cfg
# -rwx------. 1 lonny      nobody 4267 Mar  1  2021 2021/09/20210921/2021.264.03/seabird25p.cfg
# -rwx------. 1 lonny      nobody 4267 Mar  1  2021 2021/10/20211018/2021.291.00/seabird25p.cfg
# -rwx------. 1 lonny      nobody 4267 Mar  1  2021 2021/11/20211103/2021.307.02/seabird25p.cfg
# -rwx------. 1 lonny      nobody 4267 Mar  1  2021 2022/03/20220302/2022.061.01/seabird25p.cfg


def _calibrated_temp_from_frequency(cf, nc):
    # From processCTD.m:
    # TC = 1./(t_a + t_b*(log(t_f0./temp_frequency)) + t_c*((log(t_f0./temp_frequency)).^2) + t_d*((log(t_f0./temp_frequency)).^3)) - 273.15;
    # From Seabird25p.cc:
    # if (*_t_coefs == 'A') {
    #   f = ::log(T_F0/f);
    #   T = 1/(T_A + (T_B + (T_C + T_D*f)*f)*f) - 273.15;
    # }
    # else if (*_t_coefs == 'G') {
    #   f = ::log(T_GF0/f);
    #   T = 1/(T_G + (T_H + (T_I + T_J*f)*f)*f) - 273.15;
    # }
    K2C = 273.15
    calibrated_temp = (
        1.0
        / (
            cf.t_a
            + cf.t_b * np.log(cf.t_f0 / nc["temp_frequency"].values)
            + cf.t_c * np.power(np.log(cf.t_f0 / nc["temp_frequency"]), 2)
            + cf.t_d * np.power(np.log(cf.t_f0 / nc["temp_frequency"]), 3)
        )
        - K2C
    )

    return calibrated_temp


def _calibrated_sal_from_cond_frequency(args, combined_nc, logger, cf, nc, temp, depth):
    # Comments carried over from doradosdp's processCTD.m:
    # Note that recalculation of conductivity and correction for thermal mass
    # are possible, however, their magnitude results in salinity differences
    # of less than 10^-4.
    # In other regions where these corrections are more significant, the
    # corrections can be turned on.
    # conductivity at S=35 psu , T=15 C [ITPS 68] and P=0 db) ==> 42.914
    sw_c3515 = 42.914
    eps = np.spacing(1)

    f_interp = interp1d(
        combined_nc["depth_time"].values.tolist(),
        combined_nc["depth_filtpres"].values,
        fill_value="extrapolate",
    )
    p1 = f_interp(nc["time"].values.tolist())
    if args.plot:
        pbeg = 0
        pend = len(combined_nc["depth_time"])
        if args.plot.startswith("first"):
            pend = int(args.plot.split("first")[1])
        plt.figure(figsize=(18, 6))
        plt.plot(
            combined_nc["depth_time"][pbeg:pend],
            combined_nc["depth_filtpres"][pbeg:pend],
            ":o",
            nc["time"][pbeg:pend],
            p1[pbeg:pend],
            "o",
        )
        plt.legend(("Pressure from parosci", "Interpolated to ctd time"))
        title = "Comparing Interpolation of Pressure to CTD Time"
        title += f" - First {pend} Points from each series"
        plt.title(title)
        plt.grid()
        logger.debug(
            f"Pausing with plot entitled: {title}." " Close window to continue."
        )
        plt.show()

    # %% Conductivity Calculation
    # cfreq=cond_frequency/1000;
    # c1 = (c_a*(cfreq.^c_m)+c_b*(cfreq.^2)+c_c+c_d*TC)./(10*(1+eps*p1));
    cfreq = nc["cond_frequency"].values / 1000.0
    c1 = (
        cf.c_a * np.power(cfreq, cf.c_m)
        + cf.c_b * np.power(cfreq, 2)
        + cf.c_c
        + cf.c_d * temp.values
    ) / (10 * (1 + eps * p1))

    # % Calculate Salinty
    # cratio = c1*10/sw_c3515; % sw_C is conductivity value at 35,15,0
    # CTD.salinity = sw_salt(cratio,CTD.temperature,p1); % (psu)
    cratio = c1 * 10 / sw_c3515
    calibrated_salinity = eos80.salt(cratio, temp, p1)

    return calibrated_salinity
