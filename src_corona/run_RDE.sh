python DE_Model_v2.py \
    --batch_size 256 \
    --encoder_size 160 \
    --encoderR_size 160 \
    --num_layer 1 \
    --hidden_dim 300 \
    --embed_size 300 \
    --lr=0.001 \
    --num_train_steps 100000 \
    --valid_freq 500 \
    --is_save 1 \
    --graph_prefix 'RDE_ubuntu_v2_' \
    --use_glove 1 \
    --dr 0.2