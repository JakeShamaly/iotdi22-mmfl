import numpy as np
import os.path
import matplotlib

from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from scipy import stats
from pathlib import Path

METRIC = "f1"  # "accuracy", "f1"
METRIC_COLUMNS = {
    "accuracy": 5,
    "f1": 6,
}
METRIC_INDEX = METRIC_COLUMNS[METRIC]

CB_color_cycle = ['#ff7f00', '#377eb8',
                  '#f781bf', '#a65628', '#984ea3',
                  '#999999', '#e41a1c', '#dede00', '#4daf4a']

cross_selected = {
    "Opp": {"acce_gyro": [
        "client_A_label_A_test_A",
        "client_AB_label_B_test_A",
        "client_ABA_label_B_test_A",
        #   "client_ABB_label_B_test_A",
        #   "client_ABAB_label_B_test_A",
        "ablation_label_B_test_A",
        "client_new_a",

        "client_B_label_B_test_B",
        "client_AB_label_A_test_B",
        # "client_ABA_label_A_test_B",
        #   "client_ABB_label_A_test_B",
        "client_ABAB_label_A_test_B",
        "ablation_label_A_test_B",
        "client_new_b",
    ]
    }
}

modality_print = {
    "acce": "Acce",
    "gyro": "Gyro",
    "mage": "Mag",
    "rgb": "RGB",
    "depth": "Depth",
}

def single_multi_modality_comparison():
    plt.figure()
    fig, ax = plt.subplots(
        nrows=1, ncols=1, figsize=(5, 3.5))

    ax.set_ylim([0.0, 1.1])
    plt.xticks(fontsize="large")
    plt.yticks(fontsize="large")


    #color_idx = 0 if k[-1] == "A" else 1
    color_idx = 1
    #linestyle = ("-" if color_idx == 0 else "dashdot")if k[8] != "_" else (
    #    "--" if color_idx == 0 else (0, (5, 10)))
    linestyle = "-"
    test_acc = []
    
    
    rep_file = "results/opp/dccae/acce_gyro/A0_B0_AB30_label_AB_test_A/results.txt"
    data = np.loadtxt(rep_file, delimiter=",")
    x_all = data[:, 0]
    #idxs_round_cut = x_all <= ROUND_CUT[dataset]["single"]
    idxs_round_cut = x_all <= 50
    x = x_all[idxs_round_cut]
    y_rep = data[idxs_round_cut, METRIC_INDEX]
    y_rep[y_rep == 0.0] = np.nan
    test_acc.append(y_rep)
    
    y = np.nanmean(np.array(test_acc), axis=0)
    
    print("X:", x)
    print("===============")
    print("Y:", y)
    
    ax.plot(
        x, y, color=CB_color_cycle[color_idx], linestyle=linestyle) #, label=legends[k]
    plt.show()
    se = stats.sem(np.array(test_acc), nan_policy="omit")
    ax.fill_between(x, y-se, y+se,
                    color=CB_color_cycle[color_idx], alpha=0.3)
    
    ax.set_xlabel("Communication rounds", fontsize="x-large")
    metric_label = "accuracy" if METRIC == "accuracy" else "$\mathregular{F_1}$"
    ax.set_ylabel(
        f"Test {metric_label}", fontsize="x-large")
    #dataset_print = dataset.replace("_", " ")
    #ax.set_title(
    #    f"{dataset_print}, {ae_print[ae]}, A: {modality_print[modalities[0]]}, B: {modality_print[modalities[1]]}")
    ax.legend(loc="lower right", fontsize="x-large")
    Path("plots").mkdir(parents=True, exist_ok=True)
    #plt.savefig(f"plots/single_multi_modality_comparison_{dataset}_{ae}_{modalities[0]}_{modalities[1]}.pdf",
    #            bbox_inches="tight")

def cross_modality_comparison():
    plt.figure()
    fig, axes = plt.subplots(
        nrows=1, ncols=2, figsize=(10, 3.7))
    modalities = ("acce", "gyro")

    schemes_test_A = {
        #"client_A_label_A_test_A": (0, "A30_B0_AB0_label_A_test_A"),
        "client_AB_label_B_test_A": (1, "A0_B0_AB30_label_B_test_A"),
        #"client_ABA_label_B_test_A": (2, "A10_B0_AB30_label_B_test_A"),
        #"client_ABB_label_B_test_A": (3, "A0_B10_AB30_label_B_test_A"),
        #"client_ABAB_label_B_test_A": (4, "A10_B10_AB30_label_B_test_A"),
        #"ablation_label_B_test_A": (5, "A30_B30_AB0_label_B_test_A"),
        "client_new_a": (6, "A0_B0_AB30_label_AB_test_A"),
    }
    schemes_test_B = {
        #"client_B_label_B_test_B": (0, "A0_B30_AB0_label_B_test_B"),
        "client_AB_label_A_test_B": (1, "A0_B0_AB30_label_A_test_B"),
        #"client_ABB_label_A_test_B": (2, "A0_B10_AB30_label_A_test_B"),
        #"client_ABA_label_A_test_B": (3, "A10_B0_AB30_label_A_test_B"),
        #"client_ABAB_label_A_test_B": (4, "A10_B10_AB30_label_A_test_B"),
        #"ablation_label_A_test_B": (5, "A30_B30_AB0_label_A_test_B"),
        "client_new_b": (6, "A0_B0_AB30_label_AB_test_B"),
    }
    legends = {
        "client_A_label_A_test_A": "$\mathregular{UmFL_A}$",
        "client_AB_label_B_test_A": "$\mathregular{MmFL_{AB}-L_B-T_A}$",
        "client_ABA_label_B_test_A": "$\mathregular{MmFL_{ABA}-L_B-T_A}$",
        "client_ABB_label_B_test_A": "$\mathregular{MmFL_{ABB}-L_B-T_A}$",
        "client_ABAB_label_B_test_A": "$\mathregular{MmFL_{ABAB}-L_B-T_A}$",
        "ablation_label_B_test_A": "$\mathregular{Abl-L_B-T_A}$",
        "client_B_label_B_test_B": "$\mathregular{UmFL_B}$",
        "client_AB_label_A_test_B": "$\mathregular{MmFL_{AB}-L_A-T_B}$",
        "client_ABB_label_A_test_B": "$\mathregular{MmFL_{ABB}-L_A-T_B}$",
        "client_ABA_label_A_test_B": "$\mathregular{MmFL_{ABA}-L_A-T_B}$",
        "client_ABAB_label_A_test_B": "$\mathregular{MmFL_{ABAB}-L_A-T_B}$",
        "ablation_label_A_test_B": "$\mathregular{Abl-L_A-T_B}$",
        "client_new_a": "$\mathregular{?}$",
        "client_new_b": "$\mathregular{?}$",
    }

    groups = (schemes_test_A, schemes_test_B)
    for col, schemes in enumerate(groups):
        ax = axes[col]
        ax.set_ylim([0.0, 1.1])
        plt.xticks(fontsize="large")
        plt.yticks(fontsize="large")
        
        for k in schemes:
            if k not in cross_selected["Opp"][f"{modalities[0]}_{modalities[1]}"]:
                #print(k)
                continue
            color_idx = schemes[k][0]
            linestyle = (
                "-" if color_idx == 1 else "dashdot") if color_idx != 0 and color_idx != 5 else "--" if color_idx == 0 else "dotted"
            test_acc = []
            
            
            if "ablation" not in k:
                rep_file = os.path.join(
                    "results", "opp", "dccae", f"{modalities[0]}_{modalities[1]}", schemes[k][1], "results.txt")
            else:
                rep_file = os.path.join(
                    "results", "opp", "ablation", f"{modalities[0]}_{modalities[1]}", schemes[k][1], "results.txt")
            data = np.loadtxt(rep_file, delimiter=",")
            x_all = data[:, 0]
            #idxs_round_cut = x_all <= ROUND_CUT[dataset]["cross"]
            idxs_round_cut = x_all <= 50
            x = x_all[idxs_round_cut]
            y_rep = data[idxs_round_cut, METRIC_INDEX]
            y_rep[y_rep == 0.0] = np.nan
            test_acc.append(y_rep)
                
                
            y = np.nanmean(np.array(test_acc), axis=0)
            ax.plot(
                x, y, color=CB_color_cycle[color_idx], linestyle=linestyle, label=legends[k])
            se = stats.sem(np.array(test_acc), nan_policy="omit")
            ax.fill_between(x, y-se, y+se,
                            color=CB_color_cycle[color_idx], alpha=0.3)
        ax.set_xlabel("Communication rounds", fontsize="x-large")
        metric_label = "accuracy" if METRIC == "accuracy" else "$\mathregular{F_1}$"
        ax.set_ylabel(
            f"Test {metric_label}", fontsize="x-large")
        dataset_print = "Opp"
        ae_print = "DCCAE"
        ax.set_title(
            f"{dataset_print}, {ae_print}, A: {modality_print[modalities[0]]}, B: {modality_print[modalities[1]]}")
        ax.legend(loc="lower right", fontsize="x-large")
    Path("plots").mkdir(parents=True, exist_ok=True)
    plt.show()
    #plt.savefig(f"plots/cross_modality_comparison_{"Opp"}_{"ae"}_{modalities[0]}_{modalities[1]}.pdf",
    #            bbox_inches="tight")

def main():
    single_multi_modality_comparison()
    #cross_modality_comparison()


if __name__ == "__main__":
    main()
