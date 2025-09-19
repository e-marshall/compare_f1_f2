from matplotlib import pyplot as plt

def plot_f1_f2_diffs_for_icesheet(f1_obj, f2_obj, icesheet, scenario):

    f1_global = getattr(f1_obj, f'ds_processed_global_{icesheet}')
    f2_global = getattr(f2_obj, f'ds_global_{icesheet}')

    f1_local = getattr(f1_obj, f'ds_processed_local_{icesheet}')
    f2_local = getattr(f2_obj, f'ds_local_{icesheet}')

    fig, axs = plt.subplots(ncols=2, nrows=2, figsize=(12,7),
                            constrained_layout=True)

    # column centers in figure coordinates are ~0.25 and ~0.75 for a 2-column grid
    fig.text(0.5, 1.0, "Global", ha="center", va="bottom", fontsize=14, color='crimson', fontweight='bold')
    fig.text(0.5, 0.5, "Local", ha="center", va="bottom", fontsize=14, color='crimson', fontweight='bold')
    
    global_diff = (f2_global['sea_level_change'] - f1_global['sea_level_change'])

    global_row = 0
    local_row = 1
    cmap_col = 1
    hist_col = 0

    p_global = global_diff.plot(ax=axs[global_row,cmap_col])

    cbar_global = p_global.colorbar
    cbar_global.set_label('sea level change [mm]', fontsize=14)
    cbar_global.formatter.set_useOffset(False)
    cbar_global.update_ticks()
    global_diff.plot.hist(ax=axs[global_row,hist_col], bins=20)
    axs[global_row,hist_col].ticklabel_format(useOffset=False)

    local_diff = (f2_local['sea_level_change'] - f1_local['sea_level_change'])
    p_local = local_diff.plot(ax=axs[local_row,cmap_col])

    cbar_local = p_local.colorbar
    cbar_local.set_label('sea level change [mm]', fontsize=14)

    cbar_local.formatter.set_useOffset(False)
    cbar_local.update_ticks()
    local_diff.plot.hist(ax=axs[local_row,hist_col], bins=20)
    axs[local_row,hist_col].ticklabel_format(useOffset=False)

    axs[global_row][cmap_col].set_title(None)
    axs[global_row][hist_col].set_title(None)
    axs[local_row][cmap_col].set_title(None)
    axs[local_row][hist_col].set_title(None)
    axs[global_row][cmap_col].set_ylabel(None)
    axs[local_row][cmap_col].set_ylabel(None)
    axs[global_row][hist_col].set_xlabel('Sea level change [mm]', fontsize=14)
    axs[local_row][hist_col].set_xlabel('Sea level change [mm]', fontsize=14)
    fig.supylabel('Sample')
    title_str = f'Difference between projected sea level contribution btw Facts v2 and Facts v1 \n Ice sheet: {icesheet}, scenario: {scenario} --  Med Global: {global_diff.median().values:.2f} mm, Med Local: {local_diff.median().values:.2f} mm'

    fig.suptitle(title_str, fontsize=16, y=1.085);