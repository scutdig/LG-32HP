from pyhcl import *


# ///////////////////////////////////////////////////
# # E203Biu module parameters
# basic parameters
E203_ADDR_SIZE = 32
E203_XLEN = 32
# WMASK_SIZE = E203_XLEN/8
WMASK_SIZE = 4

# localparam
BIU_ARBT_I_NUM = 2
BIU_ARBT_I_PTR_W = 1

# BIU_SPLT_I_NUM_0 = 4
# BIU_SPLT_I_NUM_1 = 5
# BIU_SPLT_I_NUM_2 = 6
BIU_SPLT_I_NUM = 6


# ///////////////////////////////////////////////////





# # ///////////////////////////////////////////////////
# # sirv_gnrl_icb_arbt module parameters
#
# ## default parameters
# ARBT_SCHEME = 0
# ALLOW_0CYCL_RSP = 1
# FIFO_OUTS_NUM = 1
# FIFO_CUT_READY = 0
# ARBT_NUM = 4
# ARBT_PTR_W = 2
# USR_W = 1
# AW = 32
# DW = 64
#
# ## called parameters
# ARBT_SCHEME = 0
# ALLOW_0CYCL_RSP = 0
# FIFO_OUTS_NUM = 1
# FIFO_CUT_READY = 1
# ARBT_NUM = 2
# ARBT_PTR_W = 1
# USR_W = 1
# AW = 32
# DW = 32
# # ///////////////////////////////////////////////////
#
# # ///////////////////////////////////////////////////
# # sirv_gnrl_icb_buffer module parameters
#
# ## default parameters
# OUTS_CNT_W = 1
# AW = 32
# DW = 32
# CMD_DP = 0
# RSP_DP = 0
# CMD_CUT_READY = 0
# RSP_CUT_READY = 0
# USR_W = 1
#
# ## called parameters
# OUTS_CNT_W = 1
# AW = 32
# DW = 32
# CMD_DP = 1
# RSP_DP = 1
# CMD_CUT_READY = 1
# RSP_CUT_READY = 1
# USR_W = 1
# # ///////////////////////////////////////////////////
#
# # ///////////////////////////////////////////////////
# # sirv_gnrl_icb_splt module parameters
#
# ## default parameters
# ALLOW_DIFF = 1
# ALLOW_0CYCL_RSP = 1
# FIFO_OUTS_NUM = 8
# FIFO_CUT_READY = 0
# SPLT_NUM = 4
# SPLT_PTR_W = 4
# SPLT_PTR_1HOT = 1
# USR_W = 1
# AW = 32
# DW = 64
#
# ## called parameters
# ALLOW_DIFF = 0
# ALLOW_0CYCL_RSP = 1
# FIFO_OUTS_NUM = 1
# FIFO_CUT_READY = 1
# SPLT_NUM = 6
# SPLT_PTR_W = 6
# SPLT_PTR_1HOT = 1
# USR_W = 1
# AW = 32
# DW = 32
# # ///////////////////////////////////////////////////

# # ///////////////////////////////////////////////////
# # sirv_gnrl_pipe_stage module parameters
# ## default parameters
# CUT_READY = 0
# DP = 1
# DW = 32
#
# ## called parameters
# CUT_READY = 0
# DP = 1
# DW = 2
# # ///////////////////////////////////////////////////

# # ///////////////////////////////////////////////////
# # sirv_gnrl_fifo module parameters
# ## default parameters
# CUT_READY = 0
# MSKO = 0
# DP   = 8
# DW   = 32
#
# ## called parameters
# CUT_READY = 0
# MSKO = 0
# DP   = 1
# DW   = 2
# # ///////////////////////////////////////////////////

