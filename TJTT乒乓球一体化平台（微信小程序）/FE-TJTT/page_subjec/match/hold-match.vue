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
					<view class="hint">举办赛事</view>
					<view class="form-group">
						<image class="images" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/logo1.1.png" mode="" />
						<view class="input_section">
							<view class="title ipt">* 赛事名称：</view>
							<input maxlength="100" class="ipt tpyA" v-model="title" placeholder="请输入赛事名称" />
						</view>
						<view class="input_section">
							<view class="title ipt">赛事简介：</view>
							<input maxlength="100" class="ipt tpyA" v-model="description" placeholder="请输入赛事简介" />
						</view>
						<view class="input_section">
							<view class="title ipt">* 赛事类型：</view>
							<radio-group @change="which_match_type">
								<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="男子单打" color="#FFCC33" style="transform:scale(0.7)" />男子单打<br/>
								</label>
								<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="女子单打" color="#FFCC33" style="transform:scale(0.7)" />女子单打<br/>
								</label>
								<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="混合单打" color="#FFCC33" style="transform:scale(0.7)" />混合单打<br/>
								</label>
								<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="男子团体" color="#FFCC33" style="transform:scale(0.7)" />男子团体<br/>
								</label>
								<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="女子团体" color="#FFCC33" style="transform:scale(0.7)" />女子团体<br/>
								</label>
								<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="混合团体" color="#FFCC33" style="transform:scale(0.7)" />混合团体
								</label>
							</radio-group>
						</view>
						<view class="input_section">
							<view class="title ipt">* 赛制：</view>
							<radio-group @change="which_system">
								<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="小组循环赛+淘汰赛" color="#FFCC33" style="transform:scale(0.7)" />小组循环赛+淘汰赛<br/>
								</label>
								<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="淘汰赛" color="#FFCC33" style="transform:scale(0.7)" />淘汰赛<br/>
								</label>
								<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="大循环" color="#FFCC33" style="transform:scale(0.7)" />大循环<br/>
								</label>
								<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="小组循环赛（不决名次）" color="#FFCC33" style="transform:scale(0.7)" />小组循环赛（不决名次）<br/>
								</label>
								<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="其他" color="#FFCC33" style="transform:scale(0.7)" />其他
								</label>
							</radio-group>
						</view>
						<view class="input_section">
							<view class="title ipt">* 所在地区：</view>
							<input maxlength="100" class="ipt tpyA" v-model="address" placeholder="请输入赛事所在地区" />
						</view>
						<view class="input_section">
							<view class="title ipt">* 主办方：</view>
							<radio-group @change="which_organ_id">
								<view v-for="(organ, index) in this.organs" :key="index">
									<label class="radio" style="margin-left: 15rpx;">
										<radio v-bind:value="organ.id" color="#FFCC33" style="transform:scale(0.7)" />{{organ.organname}}
									</label>
								</view>
							</radio-group>
						</view>
						<view class="input_section">
							<view class="title ipt">* 比赛时间：</view>
							<input maxlength="100" class="ipt tpyA" v-model="match_time" placeholder="YYYY-MM-DD H:M:S" />
						</view>
						<view class="input_section">
							<view class="title ipt">* 比赛地点：</view>
							<input maxlength="100" class="ipt tpyA" v-model="place" placeholder="请输入比赛地点" />
						</view>
						<view class="input_section">
							<view class="title ipt">* 报名开始时间：</view>
							<input maxlength="100" class="ipt tpyA" v-model="sign_start_time" placeholder="YYYY-MM-DD H:M:S" />
						</view>
						<view class="input_section">
							<view class="title ipt">* 报名截止时间：</view>
							<input maxlength="100" class="ipt tpyA" v-model="sign_end_time" placeholder="YYYY-MM-DD H:M:S" />
						</view>
						<view class="input_section">
							<view class="title ipt">* 最大参赛名额：</view>
							<input type="number" maxlength="100" class="ipt tpyA" v-model="participant" placeholder="团体比赛请留空" />
						</view>
						<view class="input_section">
							<view class="title ipt">* 报名费：</view>
							<input type="number" maxlength="100" class="ipt tpyA" v-model="fee" placeholder="请输入报名费(元)" />
						</view>
						<view class="input_section">
							<view class="title ipt">* 选手报名限制：</view>
							<radio-group @change="which_restriction">
								<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="无限制" color="#FFCC33" style="transform:scale(0.7)" />无限制<br/>
								</label>
								<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="限制（仅）男子" color="#FFCC33" style="transform:scale(0.7)" />限制（仅）男子<br/>
								</label>
								<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="限制（仅）女子" color="#FFCC33" style="transform:scale(0.7)" />限制（仅）女子<br/>
								</label>
								<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="限制（仅）学生" color="#FFCC33" style="transform:scale(0.7)" />限制（仅）学生<br/>
								</label>
								<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="限制（仅）教师" color="#FFCC33" style="transform:scale(0.7)" />限制（仅）教师<br/>
								</label>
								<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="积分限制" color="#FFCC33" style="transform:scale(0.7)" />积分限制
								</label>
								<view style="display: flex; align-items: center;">
									<input type="number" maxlength="100" class="ipt tpyA" style="width: 140rpx;" v-model="score_min" placeholder="最低积分" /> ~ <input type="number" maxlength="100" class="ipt tpyA" style="width: 140rpx;" v-model="score_max" placeholder="最高积分" />
								</view>
							</radio-group>
						</view>
						<view class="input_section">
							<view class="title ipt">冠军奖品：</view>
							<input maxlength="100" class="ipt tpyA" v-model="prize_for_first" placeholder="请输入冠军奖品" />
						</view>
						<view class="input_section">
							<view class="title ipt">亚军奖品：</view>
							<input maxlength="100" class="ipt tpyA" v-model="prize_for_second" placeholder="请输入亚军奖品" />
						</view>
						<view class="input_section">
							<view class="title ipt">季军奖品：</view>
							<input maxlength="100" class="ipt tpyA" v-model="prize_for_third" placeholder="请输入季军奖品" />
						</view>
						<view class="input_section">
							<view class="title ipt">备注：</view>
							<textarea maxlength="-1" class="ipt tpyA" style="height: 150rpx;" v-model="additional_info" placeholder="请输入赛事备注" />
						</view>
					</view>
					<button class="btn round" style="background-color: #f05b05;" @click="confirm_hold">确认举办</button>
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
			fetch_data("POST", "fetch_organs", null, "competition", res => {
				this.organs = res.data.organs;
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

			confirm_hold() {
				wx.showToast({
					title: '举办中',
					icon: 'loading',
					duration: 100000,
				});
				let data = {
					"my_id": this.user.id,
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
				fetch_data("POST", "hold_match", data, "competition", res => {
					console.log(res.data.message);
					wx.showToast({
						title: res.data.message,
						icon: "none",
						duration: 1000,
					});
					if (res.data.status == 200){
						setTimeout(() => {
							uni.reLaunch({
								url: '/page_subjec/match/index',
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