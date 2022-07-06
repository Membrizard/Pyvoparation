from pathlib import Path

from pytest import fixture

from conditions import Conditions
from membrane import Membrane
from mixtures import Composition, CompositionType, Mixtures
from permeance import Permeance
from pervaporation import Pervaporation


@fixture
def test_process():

    membrane = Membrane.load(Path("tests/default_membranes/Pervap_4101"))

    pv = Pervaporation(
        membrane=membrane,
        mixture=Mixtures.H2O_EtOH,
    )

    con = Conditions(
        membrane_area=0.017,
        initial_feed_temperature=368.15,
        initial_feed_amount=1.5,
        initial_feed_composition=Composition(p=0.1, type=CompositionType.weight),
        permeate_pressure=0,
    )

    return pv.non_ideal_isothermal_process(
        conditions=con,
        diffusion_curve_set=membrane.diffusion_curve_sets[0],
        initial_permeances=(
            Permeance(0.0153),
            Permeance(0.00000632),
        ),
        number_of_steps=50,
        delta_hours=0.2,
    )


def test_get_separation_factor(test_process):

    validation_separation_factor = [
        5263.699517263321,
        5278.0243192337875,
        5309.558777004775,
        5340.893226599023,
        5371.940132746308,
        5402.696055009312,
        5433.1582610674795,
        5463.324315794544,
        5493.192071404825,
        5522.759659270987,
        5552.025481500611,
        5580.988202308215,
        5609.64673922406,
        5638.000254178127,
        5666.048144498384,
        5693.7900338595555,
        5721.225763207566,
        5748.355381703007,
        5775.1791377008785,
        5801.69746979535,
        5827.910997956347,
        5853.8205147757435,
        5879.426976844248,
        5904.731496277745,
        5929.735332401844,
        5954.439883619294,
        5978.846679461102,
        6002.957372839159,
        6026.773732503352,
        6050.29763571401,
        6073.53106113338,
        6096.476081943555,
        6119.134859186403,
        6141.509635337098,
        6163.60272810702,
        6185.416524475848,
        6206.95347495236,
        6228.216088067973,
        6249.206925089913,
        6269.928594964109,
        6290.383749471532,
        6310.575078606736,
        6330.505306163056,
        6350.177185531709,
        6369.593495693836,
        6388.757037423427,
        6407.670629666507,
        6426.337106122371,
        6444.759311995396,
        6462.940100926677,
    ]

    for i in range(len(test_process.get_separation_factor)):
        assert (
            abs(test_process.get_separation_factor[i] - validation_separation_factor[i])
            < 1e-3
        )


def test_get_psi(test_process):
    validation_data = [
        2954.01414931,
        2938.95173399,
        2918.94721531,
        2898.52844706,
        2877.74193841,
        2856.61143261,
        2835.16017013,
        2813.41097018,
        2791.38620027,
        2769.10774857,
        2746.59699931,
        2723.87481134,
        2700.96149957,
        2677.87681934,
        2654.63995336,
        2631.26950137,
        2607.78347206,
        2584.19927745,
        2560.53372925,
        2536.80303735,
        2513.02281013,
        2489.20805645,
        2465.37318924,
        2441.53203065,
        2417.6978183,
        2393.88321297,
        2370.10030719,
        2346.36063484,
        2322.67518164,
        2299.05439635,
        2275.50820261,
        2252.04601132,
        2228.67673357,
        2205.40879382,
        2182.2501435,
        2159.20827482,
        2136.29023466,
        2113.50263876,
        2090.85168573,
        2068.34317129,
        2045.98250227,
        2023.77471071,
        2001.72446767,
        1979.83609702,
        1958.11358897,
        1936.56061341,
        1915.180533,
        1893.97641605,
        1872.95104911,
        1852.10694921,
    ]

    test_data = test_process.get_psi
    for i in range(len(validation_data)):
        assert abs(validation_data[i] - test_data[i]) < 1e-3


def test_get_selectivity(test_process):
    validation_selectivity = [
        2420.8860759493673,
        2420.8860759493673,
        2428.781842974585,
        2436.5999024793805,
        2444.302218933008,
        2451.8891117709886,
        2459.3611584407636,
        2466.7190067365445,
        2473.9633700517147,
        2481.095023562955,
        2488.114800470311,
        2495.023588298794,
        2501.8223252703406,
        2508.5119967541073,
        2515.0936318020417,
        2521.568299775823,
        2527.9371070703523,
        2534.201193938171,
        2540.361731418375,
        2546.419918372889,
        2552.376978632244,
        2558.234158252372,
        2563.9927228833394,
        2569.6539552503928,
        2575.2191527471846,
        2580.6896251405983,
        2586.066692386184,
        2591.3516825528377,
        2596.545929855039,
        2601.650772790678,
        2606.667552382229,
        2611.597610518847,
        2616.44228839673,
        2621.2029250549976,
        2625.8808560041475,
        2630.4774119440904,
        2634.993917568684,
        2639.4316904536176,
        2643.792040024467,
        2648.0762666017426,
        2652.285660519724,
        2656.421501315913,
        2660.4850569879472,
        2664.4775833148697,
        2668.4003232396817,
        2672.2545063101743,
        2676.0413481751043,
        2679.7620501328297,
        2683.4177987296193,
        2687.0097654049187,
    ]
    for i in range(len(test_process.get_selectivity)):
        assert (test_process.get_selectivity[i] - validation_selectivity[i]) < 1e-3
