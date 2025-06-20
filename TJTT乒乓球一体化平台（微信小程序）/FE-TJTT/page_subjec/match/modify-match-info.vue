<template>
	<view class="main">
		<view class="main">
			<view class="pagenation">
				<view class="pagenation_back" @tap="backref()">
					<image class="back_arrow" src="..\..\static\tabbar\back.png" mode="" />
				</view>
			</view>
			<view v-if="!hide_this" class="login">
				<view class="kuang shadow">
					<view class="hint">修改赛事信息</view>
					<view class="form-group">
						<image class="images" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/logo1.1.png" mode="" />
						<view class="input_section">
							<view class="title ipt ">赛事名称：</view>
							<input maxlength="30" class="ipt tpyA" v-model="title" v-bind:placeholder="match.title" />
						</view>
						<view class="input_section">
							<view class="title ipt ">赛事简介：</view>
							<input maxlength="30" class="ipt tpyA" v-model="description" v-bind:placeholder="match.description" />
						</view>
						<view class="input_section">
							<view class="title ipt">赛事类型：</view>
							<radio-group @change="which_match_type">
								<label v-if="match.match_type=='男子单打'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="男子单打" color="#FFCC33" style="transform:scale(0.7)" checked />男子单打<br/>
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="男子单打" color="#FFCC33" style="transform:scale(0.7)" />男子单打<br/>
								</label>
								<label v-if="match.match_type=='女子单打'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="女子单打" color="#FFCC33" style="transform:scale(0.7)" checked />女子单打<br/>
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="女子单打" color="#FFCC33" style="transform:scale(0.7)" />女子单打<br/>
								</label>
								<label v-if="match.match_type=='混合单打'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="混合单打" color="#FFCC33" style="transform:scale(0.7)" checked />混合单打<br/>
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="混合单打" color="#FFCC33" style="transform:scale(0.7)" />混合单打<br/>
								</label>
								<label v-if="match.match_type=='男子团体'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="男子团体" color="#FFCC33" style="transform:scale(0.7)" checked />男子团体<br/>
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="男子团体" color="#FFCC33" style="transform:scale(0.7)" />男子团体<br/>
								</label>
								<label v-if="match.match_type=='女子团体'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="女子团体" color="#FFCC33" style="transform:scale(0.7)" checked />女子团体<br/>
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="女子团体" color="#FFCC33" style="transform:scale(0.7)" />女子团体<br/>
								</label>
								<label v-if="match.match_type=='混合团体'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="混合团体" color="#FFCC33" style="transform:scale(0.7)" checked />混合团体
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="混合团体" color="#FFCC33" style="transform:scale(0.7)" />混合团体
								</label>
							</radio-group>
						</view>
						<view class="input_section">
							<view class="title ipt">赛制：</view>
							<radio-group @change="which_system">
								<label v-if="match.system=='小组循环赛+淘汰赛'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="小组循环赛+淘汰赛" color="#FFCC33" style="transform:scale(0.7)" checked />小组循环赛+淘汰赛<br/>
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="小组循环赛+淘汰赛" color="#FFCC33" style="transform:scale(0.7)" />小组循环赛+淘汰赛<br/>
								</label>
								<label v-if="match.system=='淘汰赛'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="淘汰赛" color="#FFCC33" style="transform:scale(0.7)" checked />淘汰赛<br/>
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="淘汰赛" color="#FFCC33" style="transform:scale(0.7)" />淘汰赛<br/>
								</label>
								<label v-if="match.system=='大循环'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="大循环" color="#FFCC33" style="transform:scale(0.7)" checked />大循环<br/>
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="大循环" color="#FFCC33" style="transform:scale(0.7)" />大循环<br/>
								</label>
								<label v-if="match.system=='小组循环赛（不决名次）'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="小组循环赛（不决名次）" color="#FFCC33" style="transform:scale(0.7)" checked />小组循环赛（不决名次）<br/>
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="小组循环赛（不决名次）" color="#FFCC33" style="transform:scale(0.7)" />小组循环赛（不决名次）<br/>
								</label>
								<label v-if="match.system=='其他'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="其他" color="#FFCC33" style="transform:scale(0.7)" checked />其他
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="其他" color="#FFCC33" style="transform:scale(0.7)" />其他
								</label>
							</radio-group>
						</view>
						<view class="input_section">
							<view class="title ipt ">所在地区：</view>
							<input maxlength="30" class="ipt tpyA" v-model="address" v-bind:placeholder="user.address" />
						</view>
						<view class="input_section">
							<view class="title ipt">主办方：</view>
							<radio-group @change="which_organ_id">
								<view v-for="(organ, index) in this.organs" :key="index">
									<label v-if="match.organ_id==organ.id" class="radio" style="margin-left: 15rpx;">
										<radio v-bind:value="organ.id" color="#FFCC33" style="transform:scale(0.7)" checked />{{organ.organname}}
									</label>
									<label v-else class="radio" style="margin-left: 15rpx;">
										<radio v-bind:value="organ.id" color="#FFCC33" style="transform:scale(0.7)" />{{organ.organname}}
									</label>
								</view>
							</radio-group>
						</view>
						<view class="input_section">
							<view class="title ipt ">比赛时间：</view>
							<input maxlength="30" class="ipt tpyA" v-model="match_time" placeholder="YYYY-MM-DD H:M:S" />
						</view>
						<view class="input_section">
							<view class="title ipt ">比赛地点：</view>
							<input maxlength="30" class="ipt tpyA" v-model="place" v-bind:placeholder="match.place" />
						</view>
						<view class="input_section">
							<view class="title ipt ">报名开始时间：</view>
							<input maxlength="30" class="ipt tpyA" v-model="sign_start_time" placeholder="YYYY-MM-DD H:M:S" />
						</view>
						<view class="input_section">
							<view class="title ipt ">报名截止时间：</view>
							<input maxlength="30" class="ipt tpyA" v-model="sign_end_time" placeholder="YYYY-MM-DD H:M:S" />
						</view>
						<view class="input_section">
							<view class="title ipt ">最大参赛名额：</view>
							<input maxlength="30" class="ipt tpyA" v-model="participant" v-bind:placeholder="match.participant" />
						</view>
						<view class="input_section">
							<view class="title ipt ">报名费：</view>
							<input maxlength="30" class="ipt tpyA" v-model="fee" v-bind:placeholder="match.fee" />
						</view>
						<view class="input_section">
							<view class="title ipt">选手报名限制：</view>
							<radio-group @change="which_restriction">
								<label v-if="match.restriction=='无限制'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="无限制" color="#FFCC33" style="transform:scale(0.7)" checked />无限制<br/>
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="无限制" color="#FFCC33" style="transform:scale(0.7)" />无限制<br/>
								</label>
								<label v-if="match.restriction=='限制（仅）男子'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="限制（仅）男子" color="#FFCC33" style="transform:scale(0.7)" checked />限制（仅）男子<br/>
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="限制（仅）男子" color="#FFCC33" style="transform:scale(0.7)" />限制（仅）男子<br/>
								</label>
								<label v-if="match.restriction=='限制（仅）女子'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="限制（仅）女子" color="#FFCC33" style="transform:scale(0.7)" checked />限制（仅）女子<br/>
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="限制（仅）女子" color="#FFCC33" style="transform:scale(0.7)" />限制（仅）女子<br/>
								</label>
								<label v-if="match.restriction=='限制（仅）学生'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="限制（仅）学生" color="#FFCC33" style="transform:scale(0.7)" checked />限制（仅）学生<br/>
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="限制（仅）学生" color="#FFCC33" style="transform:scale(0.7)" />限制（仅）学生<br/>
								</label>
								<label v-if="match.restriction=='限制（仅）教师'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="限制（仅）教师" color="#FFCC33" style="transform:scale(0.7)" checked />限制（仅）教师<br/>
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="限制（仅）教师" color="#FFCC33" style="transform:scale(0.7)" />限制（仅）教师<br/>
								</label>
								<label v-if="match.restriction=='积分限制'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="积分限制" color="#FFCC33" style="transform:scale(0.7)" checked />积分限制
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="积分限制" color="#FFCC33" style="transform:scale(0.7)" />积分限制
								</label>
								<view v-if="match.restriction=='积分限制'" style="display: flex; align-items: center;">
									<input maxlength="30" class="ipt tpyA" style="width: 140rpx;" v-model="score_min" v-bind:placeholder="match.score_min" /> ~ <input maxlength="30" class="ipt tpyA" style="width: 140rpx;" v-model="score_max" v-bind:placeholder="match.score_max" />
								</view>
								<view v-else style="display: flex; align-items: center;">
									<input maxlength="30" class="ipt tpyA" style="width: 140rpx;" v-model="score_min" placeholder="最低积分" /> ~ <input maxlength="30" class="ipt tpyA" style="width: 140rpx;" v-model="score_max" placeholder="最高积分" />
								</view>
							</radio-group>
						</view>
						<view class="input_section">
							<view class="title ipt ">冠军奖品：</view>
							<input maxlength="30" class="ipt tpyA" v-model="prize_for_first" v-bind:placeholder="match.prize_for_first" />
						</view>
						<view class="input_section">
							<view class="title ipt ">亚军奖品：</view>
							<input maxlength="30" class="ipt tpyA" v-model="prize_for_second" v-bind:placeholder="match.prize_for_second" />
						</view>
						<view class="input_section">
							<view class="title ipt ">季军奖品：</view>
							<input maxlength="30" class="ipt tpyA" v-model="prize_for_third" v-bind:placeholder="match.prize_for_third" />
						</view>
						<view class="input_section">
							<view class="title ipt ">备注：</view>
							<textarea class="ipt tpyA" style="height: 150rpx;" v-model="additional_info" v-bind:placeholder="match.additional_info" />
						</view>
					</view>
					<button class="btn round" style="background-color: #f05b05;" @click="modify">确认修改</button>
				</view>
			</view>
			<view class="bottom">
			</view>
		</view>
	</view>
</template>

<script>
	import { fetch_data } from '../../static/js/ajax_request.js'
	import { login_check } from '../../static/js/login_check.js'
	import { magic } from '../../static/js/magic_power.js'
	export default {
		data() {
			return {
				message: "",
				user: "",
				match: "",
				organs: [],
				title: "",
				description: "",
				match_type: "",
				system: "",
				address: "",
				organ_id: "",
				match_time: "",
				place: "",
				sign_start_time: "",
				sign_end_time: "",
				participant: "",
				fee: "",
				restriction: "",
				prize_for_first: "",
				prize_for_second: "",
				prize_for_third: "",
				additional_info: "",
				score_min: "",
				score_max: "",
				hide_this: magic(),
			} 
		},
		onLoad() {
			login_check(user => {
				this.user = user;
			});
			if (!this.user) {
				wx.showToast({
					title: "请登录",
					icon: "none",
					duration: 1500,
				});
				setTimeout(() => {
					uni.reLaunch({
						url: '/pages/login/login',
					})
				}, 1000);
			};
			
			// 获取赛事
			wx.showToast({
				title: '加载中',
				icon: 'loading',
				duration: 100000,
			});
			let match_id = uni.getStorageSync('match_id');
			fetch_data("POST", "get_this_match", {"match_id": match_id}, "competition", res => {
				this.match = res.data.match;
				wx.hideToast();
			});
			
			fetch_data("POST", "fetch_organs", null, "competition", res => {
				this.organs = res.data.organs;
				wx.hideToast();
			});
		},
		methods: {
			onInput(e) {
				this.title = e.target.value
				this.description = e.target.value
				this.address = e.target.value
				this.match_time = e.target.value
				this.place = e.target.value
				this.sign_start_time = e.target.value
				this.sign_end_time = e.target.value
				this.participant = e.target.value
				this.fee = e.target.value
				this.prize_for_first = e.target.value
				this.prize_for_second = e.target.value
				this.prize_for_third = e.target.value
				this.additional_info = e.target.value
				this.score_min = e.target.value
				this.score_max = e.target.value
			},
			
			which_match_type(e) {
				this.match_type = e.detail.value
			},
			which_system(e) {
				this.system = e.detail.value
			},
			which_organ_id(e) {
				this.organ_id = parseInt(e.detail.value)
			},
			which_restriction(e) {
				this.restriction = e.detail.value
			},

			backref() {
				uni.navigateBack({
					delta: 1
				});
			},

			modify() {
				wx.showToast({
					title: '修改中',
					icon: 'loading',
					duration: 100000,
				});
				let data = {
					"my_id": this.user.id,
					"match_id": this.match.id,
					"title": this.title,
					"description": this.description,
					"match_type": this.match_type,
					"system": this.system,
					"address": this.address,
					"organ_id": this.organ_id,
					"match_time": this.match_time,
					"place": this.place,
					"sign_start_time": this.sign_start_time,
					"sign_end_time": this.sign_end_time,
					"participant": this.participant,
					"fee": this.fee,
					"restriction": this.restriction,
					"prize_for_first": this.prize_for_first,
					"prize_for_second": this.prize_for_second,
					"prize_for_third": this.prize_for_third,
					"additional_info": this.additional_info,
					"score_min": this.score_min,
					"score_max": this.score_max,
				}
				fetch_data("POST", "modify_match_info", data, "competition", res => {
					wx.showToast({
						title: res.data.message,
						icon: "none",
						duration: 1000,
					});
					if (res.data.status == 200){
						setTimeout(() => {
							uni.reLaunch({
								url: '/page_subjec/match/detail',
							})
						}, 1000);
					}
				})
			},
		}
	}
</script>

<style lang="scss">
	.pagenation {
		.pagenation_back {
			position: absolute;
			display: flex;
			justify-content: center;
			align-items: center;
			width: 76rpx;
			height: 76rpx;
			border-radius: 50%;
			border: 1rpx solid #bcbcbc;
			margin: 75rpx 40rpx;

			.back_arrow {
				width: 50rpx;
				height: 50rpx;
			}
		}
	}
</style>

<style>
	.main {
		width: 100%;
		height: 100%;
		background: linear-gradient(135deg, #FEF2DA, #FFD5A4);
		display: flex;
		flex-direction: column;
		justify-content: flex-start;
	}

	.main .login {
		margin-top: 150rpx;
		display: flex;
		flex-direction: column;
		justify-content: flex-start;
		align-items: center;
		flex: 1;
	}

	.main .login .kuang {
		width: 660rpx;
		background-color: #fff;
		height: 100%;
		margin-top: 85rpx;
		border-radius: 20rpx;
		/* display: flex; */
		flex-direction: column;
		justify-content: space-between;
		align-items: center;
		padding: 50rpx 20rpx;
	}

	.main .login .kuang .btn {
		width: 85%;
		color: #fff;
		font-size: 32rpx;
		margin: 40rpx;
	}

	.main .login .kuang .hint {
		width: 100%;
		color: black;
		font-size: 50rpx;
		font-weight: bold;
		text-align: center;
	}

	.main .login .kuang .return {
		width: 100%;
		color: #fef2da;
		font-size: 30rpx;
		text-align: center;
		font-size: 26rpx;
	}

	.main .avatar-open {
		width: 180rpx;
		height: 180rpx;
		clip-path: circle(90rpx at center);
	}

	.main .bottom {
		width: 100%;
		align-self: flex-end;
		font-size: 26rpx;
		height: 120rpx;
		text-align: center;
		color: #fff;
		display: flex;
		flex-direction: column;
	}

	.form-group {
		margin: 40rpx;
		text-align: center;
	}

	.form-group .title {
		white-space: nowrap;
		font-weight: normal;
	}

	.form-group .input_section {
		margin: 40rpx;
		display: flex;
		flex-direction: row;
		text-align: justify;
	}

	.title {
		line-height: 42rpx !important;
	}

	.images {
		width: 160rpx;
		height: 160rpx;
		border-radius: 50%;
	}

	.tpyA {
		padding: 0px 20rpx;
	}

	.ipt {
		font-size: 26rpx;
	}
</style>