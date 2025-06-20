<template>
	<div>
		<div v-if="!hide_this" class="header">
			<div class="flex">
				<div class="left" @click="avatar_operation">
					<img v-if="user_x.profile_img" class="user" style="border-radius: 50%;"
						:src="user_x.profile_img"
						alt="" />
					<img v-else-if="user_x.gender == '男'" class="user" style="border-radius: 50%;"
						src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/avatars/male.jpg"
						alt="" />
					<img v-else-if="user_x.gender == '女'" class="user" style="border-radius: 50%;"
						src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/avatars/female.jpg"
						alt="" />
				</div>
				<div class="right">
					<div class="nike">{{user_x.username}} - {{user_x.school}}</div>
					<div v-if="user_x.organ" class="model">{{user_x.organ.organname}}</div>
				</div>
			</div>
			<div class="userList flex">
				<div class="itemList">
					<p v-if="user_x.hand" class="p">{{user_x.hand}}</p>
					<p v-else class="p" style="color: red;">待完善</p>
					<div class="span">执拍手</div>
				</div>
				<div class="itemList">
					<p v-if="user_x.grip" class="p">{{user_x.grip}}</p>
					<p v-else class="p" style="color: red;">待完善</p>
					<div class="span">握拍方式</div>
				</div>
				<div class="itemList">
					<p v-if="user_x.particle" class="p">{{user_x.particle}}</p>
					<p v-else class="p" style="color: red;">待完善</p>
					<div class="span">颗粒</div>
				</div>
				<div class="itemList">
					<p class="p">{{user_x.score}}</p>
					<div class="span">TJTT积分</div>
				</div>
			</div>

			<div class="userList flex">
				<div class="itemList" style="width: 25%; white-space: nowrap;"
					v-for="(item, index) in actionList" :key="index">
					<view v-if="index==0 && !hide_this" @click="modify_user_info">
						<p class="p">
							<u-icon name="setting-fill" size="40" />
						</p>
						<div class="span">{{ item.name }}</div>
					</view>
					<view v-else-if="index==1">
						<view v-if="user_x.privacy==0" @click="set_private">
							<p class="p">
								<u-icon name="account-fill" size="40" />
							</p>
							<div class="span">{{ item.name }}</div>
						</view>
						<view v-else @click="set_public">
							<p class="p">
								<u-icon name="account" size="40" />
							</p>
							<div class="span">设为公开用户</div>
						</view>
					</view>
					<view v-else-if="index==2" @click="modify_usertype">
						<p class="p">
							<u-icon name="star-fill" size="40" />
						</p>
						<div class="span">{{ item.name }}</div>
					</view>
					<view v-else-if="index==3" @click="delete_user">
						<p class="p" style="color: red;">
							<u-icon name="person-delete-fill" size="40" />
						</p>
						<div class="span" style="color: red;">{{ item.name }}</div>
					</view>
				</div>
			</div>
			<div class="tipTitle">用户信息</div>
			<div style="margin: 30rpx;">
				<uni-table stripe emptyText="无数据" style="z-index: -1;">
					<uni-tr>
						<uni-td>
							<view class="table_head">性别</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user_x.gender}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">所在地区</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user_x.address}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">手机号</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user_x.phone}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">邮箱</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user_x.email}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">学校</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user_x.school}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">身份</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user_x.role}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">学号 / 工号</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user_x.stu_num}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr v-if="user_x.organ">
						<uni-td>
							<view class="table_head">所属组织</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user_x.organ.organname}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">执拍手</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user_x.hand}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">握拍方式</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user_x.grip}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">底板型号</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user_x.blade}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">正手胶皮</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user_x.forehand}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">反手胶皮</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user_x.backhand}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">是否带颗粒</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user_x.particle}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">权限级</view>
						</uni-td>
						<uni-td v-if="user_x.usertype=='0'">
							<view class="table_content" style="color: red;">普通用户</view>
						</uni-td>
						<uni-td v-else>
							<view class="table_content" style="color: red;">{{user_x.usertype}}级管理员</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">是否为私密用户</view>
						</uni-td>
						<uni-td v-if="user_x.privacy==1">
							<view class="table_content" style="color: red;">是</view>
						</uni-td>
						<uni-td v-else>
							<view class="table_content" style="color: red;">否</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">注册时间</view>
						</uni-td>
						<uni-td>
							<view class="table_content" style="color: red;">{{utils.format_time(user_x.join_time)}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">是否为TJTT Studio成员</view>
						</uni-td>
						<uni-td v-if="user_x.is_TJTT==0">
							<view class="table_content" style="color: red;" @click="modify_TJTTer">否</view>
						</uni-td>
						<uni-td v-else>
							<view class="table_content" style="color: red;" @click="modify_TJTTer">是</view>
						</uni-td>
					</uni-tr>
				</uni-table>
			</div>
		</div>
	</div>
</template>

<script>
	import { fetch_data } from '../../static/js/ajax_request.js'
	import { login_check } from '../../static/js/login_check.js'
	import { magic } from '../../static/js/magic_power.js'
	export default {
		data() {
			return {
				user: "",
				user_x: "",
				actionList: [{
						name: "修改用户信息",
					},
					{
						name: "设为私密用户",
					},
					{
						name: "变更用户权限级",
					},
					{
						name: "删除用户",
					},
				],
				hide_this: magic(),
			}
		},
		onLoad() {
			login_check(user => {
				this.user = user;
			});
			if (!this.user || (this.user.usertype != "K9" && this.user.usertype != "K10" && this.user.usertype !=
					"K11")) {
				wx.showToast({
					title: "权限不足",
					icon: "none",
					duration: 1500,
				});
				setTimeout(() => {
					uni.reLaunch({
						url: '/pages/index/index',
					})
				}, 1000);
			};
			// 获取用户信息
			let user_id = uni.getStorageSync("user_id");
			if (!user_id) {
				wx.showToast({
					title: "服务器繁忙，请稍后再试",
					icon: "none",
					duration: 1500,
				});
				setTimeout(() => {
					uni.reLaunch({
						url: '/page_subjec/user/user-list',
					})
				}, 1000);
			} else {
				wx.showToast({
					title: '加载中',
					icon: 'loading',
					duration: 100000,
				});
				// 防止过短时间内调用两次/get_this_user接口
				setTimeout(() => {
					fetch_data("POST", "get_this_user", {"user_id": user_id}, "user", res => {
						this.user_x = res.data.user;
						wx.hideToast();
					});
				}, 400);

			};
		},
		beforeDestroy() {
			uni.removeStorageSync('user_id');
		},

		methods: {
			avatar_operation() {
				wx.showActionSheet({
					itemList: ['查看头像', '更换头像', '删除头像'],
					success: (res) => {
						if (!res.cancel) {
							let avatarUrl = this.user_x.profile_img;
							if (res.tapIndex == 0) {
								if (avatarUrl) {
									wx.previewImage({
										urls: [avatarUrl],
										current: avatarUrl,
									});
								}
								else {
									wx.showToast({
										title: "该用户还未上传头像",
										icon: "none",
										duration: 1000,
									});
									return;
								};
							}
							else if (res.tapIndex == 1) {
								wx.showModal({
									title: '请输入用户头像URL',
									editable: true,
									success: res => {
										if (res.confirm) {
											let data = {
												"my_id": this.user.id,
												"user_id": this.user_x.id,
												"profile_img": res.content,
											}
											fetch_data("POST", "modify_user_profile_img", data, "user", res => {
												wx.showToast({
													title: res.data.message,
													icon: "none",
													duration: 1000,
												});
												if (res.data.status == 200) {
													setTimeout(() => {
														uni.reLaunch({
															url: '/page_subjec/user/user-detail',
														})
													}, 1000);
												}
											})
										}
									}
								})
							}
							else if (res.tapIndex == 2) {
								if (!avatarUrl) {
									wx.showToast({
										title: "该用户还未上传头像",
										icon: "none",
										duration: 1000,
									});
									return;
								}
								wx.showModal({
									title: '删除头像',
									content: '确定删除该用户头像？',
									success: res => {
										if (res.confirm) {
											let data = {
												"my_id": this.user.id,
												"user_id": this.user_x.id,
											}
											fetch_data("POST", "delete_user_profile_img", data, "user", res => {
												wx.showToast({
													title: res.data.message,
													icon: "none",
													duration: 1000,
												});
												if (res.data.status == 200){
													setTimeout(() => {
														uni.reLaunch({
															url: '/page_subjec/user/user-detail',
														})
													}, 1000);
												}
											})
										}
									}
								})
							};
						}
					}
				})
			},
			
			modify_user_info() {
				uni.setStorageSync("user_id", this.user_x.id)
				uni.navigateTo({
					url: '/page_subjec/user/modify-user-info',
				})
			},

			set_private() {
				wx.showModal({
					title: '设为私密用户',
					content: '设为私密用户后，该用户在“积分排名”中将以“' + this.user_x.username[0] + '** ”显示。',
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user.id,
								"user_id": this.user_x.id,
								"set": "private",
							}
							fetch_data("POST", "set_privacy", data, "user", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									fetch_data("POST", "get_this_user", {
										"user_id": this.user_x.id
									}, "user", res => {
										this.user_x = res.data.user
									});
								}
							})
						}
					}
				})
			},

			set_public() {
				wx.showModal({
					title: '设为公开用户',
					content: '设为公开用户后，该用户在“积分排名”中将以全名显示。',
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user.id,
								"user_id": this.user_x.id,
								"set": "public",
							}
							fetch_data("POST", "set_privacy", data, "user", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									fetch_data("POST", "get_this_user", {
										"user_id": this.user_x.id
									}, "user", res => {
										this.user_x = res.data.user
									});
								}
							})
						}
					}
				})
			},

			modify_usertype() {
			    if (this.user.usertype !== "K11") {
			        wx.showToast({
			            title: "权限不足",
			            icon: "none",
			            duration: 1500,
			        });
			    } else {
			        wx.showActionSheet({
			            itemList: ['普通用户', 'K9级管理员', 'K10级管理员', 'K11级管理员'],
			            success: res => {
			                if (!res.cancel) {
			                    let usertypeMap = ["0", "K9", "K10", "K11"];
			                    let newType = usertypeMap[res.tapIndex];
			                    let contentMap = [
			                        `用户${this.user_x.username}原权限级"${this.user_x.usertype}"，确认变更为普通用户？`,
			                        `用户${this.user_x.username}原权限级"${this.user_x.usertype}"，确认变更为K9级管理员？`,
			                        `用户${this.user_x.username}原权限级"${this.user_x.usertype}"，确认变更为K10级管理员？`,
			                        `用户${this.user_x.username}原权限级"${this.user_x.usertype}"，确认变更为K11级管理员？`
			                    ];
			
			                    wx.showModal({
			                        title: '变更用户权限级',
			                        content: contentMap[res.tapIndex],
			                        success: res => {
			                            if (res.confirm) {
			                                let data = {
			                                    "my_id": this.user.id,
			                                    "user_id": this.user_x.id,
			                                    "usertype": newType,
			                                };
			                                fetch_data("POST", "modify_usertype", data, "user", res => {
			                                    wx.showToast({
			                                        title: res.data.message,
			                                        icon: "none",
			                                        duration: 700,
			                                    });
			                                    if (res.data.status === 200) {
			                                        fetch_data("POST", "refresh", { "my_id": this.user.id }, "user", res => {
			                                            uni.setStorageSync('user', res.data.user);
			                                        });
			                                        this.user_x.usertype = newType;
			                                    }
			                                });
			                            }
			                        }
			                    });
			                }
			            }
			        });
			    }
			},

			delete_user() {
				wx.showModal({
					title: '删除用户',
					content: '删除用户后，该用户所有信息及赛事记录将被永久清除；该操作可能导致数据库混乱、系统崩溃，请上报K11级管理员后操作',
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user.id,
								"user_id": this.user_x.id,
							}
							fetch_data("POST", "delete_user", data, "user", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									setTimeout(() => {
										uni.reLaunch({
											url: '/page_subjec/user/user-list',
										})
									}, 1000);
								}
							})
						}
					}
				})
			},
			
			modify_TJTTer() {
				if (this.user.usertype != 'K11') {
					return;
				}
				var title = null;
				var content = null;
				if (this.user_x.is_TJTT) {
					title = '移出TJTT Studio';
					content = '是否确定将该用户移出TJTT Studio';
				}
				else {
					title = '加入TJTT Studio';
					content = '是否确定将该用户加入TJTT Studio';
				}
				wx.showModal({
					title: title,
					content: content,
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user.id,
								"user_id": this.user_x.id,
							}
							fetch_data("POST", "modify_TJTTer", data, "application", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									setTimeout(() => {
										uni.reLaunch({
											url: '/pages/apps/TJTTers',
										})
									}, 1000);
								}
							})
						}
					}
				})
			},
		},
	}
</script>

// 直接挂载到template中使用
<script setup>
	import * as utils from '../../static/js/utils.js'
</script>

<style lang="scss" scoped>
	.btn-outline-sm {
		position: absolute;
		display: inline-block;
		padding: 1rem 1.5rem 1rem 1.5rem;
		border: 1px solid #f25c05;
		border-radius: 30px;
		background-color: transparent;
		color: #f25c05;
		font-weight: 600;
		font-size: 0.875rem;
		line-height: 0;
		text-decoration: none;
		transition: all 0.2s;
		top: 210rpx;
		left: 520rpx;
	}

	.btn-modify {
		position: relative;
		display: inline-block;
		padding: 1rem 1.5rem 1rem 1.5rem;
		border: 1px solid #00ffff;
		border-radius: 30px;
		background-color: transparent;
		color: #00ffff;
		font-weight: 600;
		font-size: 0.875rem;
		line-height: 0;
		text-decoration: none;
		transition: all 0.2s;
		top: 18rpx;
		left: 15rpx;
	}

	.dropdown1 {
		position: absolute;
		width: 300rpx;
		top: 1180rpx;
		z-index: 999;
	}

	.topIcon {
		margin-top: 30rpx;
	}

	.imgs {
		margin-top: 20rpx;
		width: 48%;
		border-radius: 12rpx;
		height: 190rpx;
	}

	.tipTitle {
		position: relative;
		margin-top: 25rpx;
		font-family: PingFang SC, PingFang SC;
		font-weight: 600;
		font-size: 32rpx;
		color: #212121;
		line-height: 36rpx;
		text-align: left;
		font-style: normal;
		text-transform: none;
	}

	.phBox {
		background: linear-gradient(320deg, #f7eddd 0%, #edd3bc 100%);
		border-radius: 0rpx 0rpx 20rpx 20rpx;
		box-sizing: border-box;
		padding: 26rpx 16rpx;
		padding-top: 40rpx;

		.bc {
			border-radius: 12rpx 12rpx 12rpx 12rpx;

			.text1 {
				margin-top: 4rpx;
				font-family: PingFang SC, PingFang SC;
				font-weight: bold;
				font-size: 28rpx;
				color: #282456;
				line-height: 30rpx;
				text-align: left;
				font-style: normal;
				text-transform: none;
			}

			.text2 {
				margin-top: 19rpx;
				font-family: PingFang SC, PingFang SC;
				font-weight: 600;
				font-size: 24rpx;
				color: #f25c07;
				line-height: 10rpx;
				text-align: left;
				font-style: normal;
				text-transform: none;
			}

			.text3 {
				margin-top: 27rpx;
				font-family: PingFang SC, PingFang SC;
				font-weight: 400;
				font-size: 24rpx;
				color: #666666;
				line-height: 0rpx;
				text-align: left;
				font-style: normal;
				text-transform: none;
			}

			.right {
				width: 62%;
			}

			.left {
				width: 34%;

				.bcImg {
					border-radius: 6rpx 6rpx 6rpx 6rpx;
					width: 100%;
					height: 130rpx;
				}
			}

			margin-top: 30rpx;
			background-color: white;
			box-sizing: box-sizing;
			padding: 18rpx 14rpx;
		}

		.title {
			font-family: PingFang SC, PingFang SC;
			font-weight: 600;
			font-size: 28rpx;
			color: #212121;
			line-height: 24rpx;
			text-align: left;
			font-style: normal;
			text-transform: none;
			margin-top: 20rpx;
		}
	}

	.piCon {
		width: 44rpx;
		height: 44rpx;
	}

	.table_head {
		width: 200rpx;
		text-align: center;
		font-weight: normal;
		white-space: nowrap;
		text-overflow: ellipsis;
	}

	.table_content {
		width: 400rpx;
		text-align: center;
		font-weight: bold;
		white-space: nowrap;
		text-overflow: ellipsis;
	}

	.box2 {
		.tp {
			box-sizing: box-sizing;
			padding: 0rpx 18rpx;
			margin-top: 40rpx;
		}

		.boxT {
			box-sizing: box-sizing;
			padding: 20rpx;
			background-color: #ffffff;
			width: 48%;

			border-radius: 20rpx 20rpx 20rpx 20rpx;

			.LEFTiCON {
				width: 85rpx;
				height: 85rpx;
			}

			.myPm {
				margin-left: 14rpx;
				display: inline-block;
				font-family: PingFang SC, PingFang SC;
				font-weight: 600;
				font-size: 32rpx;
				color: #212121;
				line-height: 40rpx;
				text-align: left;
				font-style: normal;
				text-transform: none;
			}

			.righttP {
				width: 60%;
				font-family: PingFang SC, PingFang SC;
				font-weight: 500;
				font-size: 28rpx;
				color: #212121;
				line-height: 28rpx;
				text-align: center;
				line-height: 40rpx;
				font-style: normal;
				text-transform: none;
			}

			.tipText {
				font-size: 28rpx;
				color: #666666;
				margin-top: 12rpx;
				margin-left: 20rpx;
			}

			.spanTip {
				color: #f25c07;
				font-weight: bold;
			}

			.tip {
				display: inline-block;
				width: 6rpx;
				height: 20rpx;
				background: #f25c07;
				border-radius: 12rpx 12rpx 12rpx 12r;
			}
		}
	}

	.userList {
		position: relative;
		box-sizing: box-sizing;
		padding: 28rpx 20rpx;
		margin-top: 20rpx;
		background: #ffffff;
		border-radius: 20rpx 20rpx 20rpx 20rpx;

		.p {
			font-family: PingFang SC, PingFang SC;
			font-weight: 600;
			font-size: 36rpx;
			color: #282456;
			line-height: 40rpx;
			text-align: center;
			font-style: normal;
			text-transform: none;
		}
	}

	.itemList {
		text-align: center;
		width: 24%;
	}

	.user {
		width: 120rpx;
		height: 120rpx;
		border-radius: 0rpx 0rpx 0rpx 0rpx;
	}

	.span {
		margin-top: 24rpx;
		font-family: PingFang SC, PingFang SC;
		font-weight: 400;
		font-size: 24rpx;
		color: #666666;
		line-height: 24rpx;
		text-align: center;
		font-style: normal;
		text-transform: none;
	}

	.header {
		background: linear-gradient(135deg, #FEF2DA, #FFD5A4);
		width: 100%;
		height: 100%;
		box-sizing: border-box;
		padding: 30rpx;

		.icon {
			margin-right: 20rpx;
			width: 37rpx;
			height: 37rpx;
		}

		.nike {
			font-family: PingFang SC, PingFang SC;
			font-weight: 600;
			font-size: 36rpx;
			color: #282456;
			line-height: 36rpx;
			text-align: left;
			font-style: normal;
			text-transform: none;
		}

		.left {
			width: 20%;
		}

		.right {
			width: 80%;
			box-sizing: border-box;
			padding-top: 20rpx;
		}

		.model {
			font-family: PingFang SC, PingFang SC;
			font-weight: 400;
			font-size: 24rpx;
			color: #666666;
			line-height: 24rpx;
			margin-top: 20rpx;
			margin-left: 8rpx;
			font-style: normal;
			text-transform: none;
		}
	}

	::v-deep .uni-table {
		background: linear-gradient(135deg, #FEF2DA, #FFD5A4);
	}
</style>