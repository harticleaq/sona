python main.py -data nipsD_offline -batch_size 128 -plot_title 'paper_0203_new' \
-max_epoch 40 -lr 1e-3 -opt Adam -test_batch_size 5000 -model deepgbm -task binary -l2_reg 1e-6 \
-test_freq 3000 -seed 1,2,3,4,5 -group_method Random -emb_epoch 2 -loss_de 2 -loss_dr 0.7 -tree_lr 0.1 \
-cate_layers 16,16 -nslices 10 -cate_embsize 2 -tree_layers 100,100,100,50 -embsize 20 -maxleaf 64 -log_freq 200 -feat_per_group 64
