<template>
	<section>
		<!--工具条-->
		<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
			<el-form :inline="true" :model="filters">
				<el-form-item>
					<el-input v-model="filters.name" placeholder="名称"></el-input>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" v-on:click="getUsers">查询</el-button>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" @click="handleAdd">新增</el-button>
				</el-form-item>
			</el-form>
		</el-col>
		<!--列表-->
		<el-table :data="users" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
			<el-table-column type="selection">
			</el-table-column>
			<el-table-column type="index">
			</el-table-column>
			<el-table-column prop="name" label="名称" sortable>
			</el-table-column>
			<el-table-column prop="subnets" label="网络地址" sortable>
			</el-table-column>
			<el-table-column prop="shared" label="共享" sortable>
			</el-table-column>
			<el-table-column prop="external" label="外网路由" sortable>
			</el-table-column>
			<el-table-column prop="status" label="状态" sortable>
			</el-table-column>
			<el-table-column prop="admin_state_up" label="管理状态" sortable>
			</el-table-column>
			<el-table-column label="操作">
				<template scope="scope">
					<el-button-group>
						<el-button size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
						<el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>
					</el-button-group>
				</template>
			</el-table-column>
		</el-table>

		<!--工具条-->
		<el-col :span="24" class="toolbar">
			<el-button type="danger" @click="batchRemove" :disabled="this.sels.length===0">批量删除</el-button>
			<el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="20" :total="total" style="float:right;">
			</el-pagination>
		</el-col>

		<!--编辑界面-->
		<el-dialog title="编辑" v-model="editFormVisible" :close-on-click-modal="false">
			<el-form :model="editForm" label-width="80px" :rules="editFormRules" ref="editForm">
				<el-form-item label="姓名" prop="name">
					<el-input v-model="editForm.name" auto-complete="off"></el-input>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="editFormVisible = false">取消</el-button>
				<el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
			</div>
		</el-dialog>

		<!--新增界面-->
		<el-dialog title="新增" v-model="addFormVisible" :close-on-click-modal="false">
			<el-form :model="addForm" :rules="addFormRules" ref="addForm">
				<el-form-item label="名称" prop="name">
					<el-input v-model="addForm.name" auto-complete="off"></el-input>
				</el-form-item>
				<el-form-item label="镜像:" prop="image">{{addForm.afin.name}}
					<el-table :data="image" highlight-current-row @current-change="handleImageCurrentChange">
						<el-table-column property="name" label="名称" width="150"></el-table-column>
						<el-table-column property="disk_format" label="格式" width="200"></el-table-column>
						<el-table-column property="visibility" label="可见"></el-table-column>
					</el-table>
				</el-form-item>
				<el-form-item label="实例类型" prop="flavor">
					<el-select v-model="addForm.affn" placeholder="请选择">
						<el-option v-for="item in flavor" :key="item.name" :label="item.name" :value="item.id">
							<span style="float: left">{{ item.name }}</span>
							<span style="float: right; color: #8492a6; font-size: 13px">{{ item.name }}</span>
						</el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="网络" prop="network">
					<el-select v-model="addForm.afnn" placeholder="请选择">
						<el-option v-for="item in network" :key="item.name" :label="item.name" :value="item.id">
							<span style="float: left">{{ item.name }}</span>
							<span style="float: right; color: #8492a6; font-size: 13px">{{ item.status }}</span>
						</el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="可用域">
					<el-select v-model="addForm.afan" placeholder="请选择">
						<el-option v-for="item in AZ" :key="item.zoneName" :label="item.zoneName" :value="item.zoneName">
							<span style="float: left">{{ item.zoneName }}</span>
							<span style="float: right; color: #8492a6; font-size: 13px">{{ item.zoneState.available }}</span>
						</el-option>
					</el-select>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="addFormVisible = false">取消</el-button>
				<el-button type="primary" @click.native="addSubmit" :loading="addLoading">提交</el-button>
			</div>
		</el-dialog>
	</section>
</template>

<script>
import util from '../../common/js/util'
//import NProgress from 'nprogress'
// import { getUserListPage, removeUser, batchRemoveUser, editUser, addUser } from '../../api/api';

export default {
	data() {
		return {
			filters: {
				name: ''
			},
			options: [{
				value: '选项1',
				label: '黄金糕'
			}, {
				value: '选项2',
				label: '双皮奶'
			}, {
				value: '选项3',
				label: '蚵仔煎'
			}, {
				value: '选项4',
				label: '龙须面'
			}, {
				value: '选项5',
				label: '北京烤鸭'
			}],
			value: '',
			users: [],
			total: 0,
			page: 1,
			listLoading: false,
			sels: [],//列表选中列

			editFormVisible: false,//编辑界面是否显示
			editLoading: false,
			editFormRules: {
				name: [
					{ required: true, message: '请输入姓名', trigger: 'blur' }
				]
			},
			//编辑界面数据
			editForm: {
				id: 0,
				name: ''
			},

			addFormVisible: false,//新增界面是否显示
			addLoading: false,
			addFormRules: {
				name: [
					{ required: true, message: '请输入姓名', trigger: 'change' }
					// ],
					// image: [
					// 	{ required: true, message: '请选择镜像', trigger: 'change'}
					// ],
					// flavor: [
					// 	{ required: true, message: '请选择实例类型', trigger: 'change'}
					// ],
					// network: [
					// 	{ required: true, message: '请选择网络', trigger: 'change'}
				]
			},
			//新增界面数据
			addForm: {
				name: '',
				afin: [],
				affn: '',
				afnn: '',
				afan: '',
			},

			image: [],
			flavor: [],
			network: [],
			AZ: []

		}
	},
	methods: {
		handleCurrentChange(val) {
			this.page = val;
			this.getUsers();
		},
		handleImageCurrentChange(val) {
			this.addForm.afin = val;
		},
		//获取network列表
		getUsers() {
			console.log('getting users now')
			let para = {
				page: this.page,
				name: this.filters.name
			};
			this.listLoading = true;
			//NProgress.start();
			this.$http.get('/api/network/list/').then((res) => {
				console.log(res.data);
				if (res.data == 'session expire') {
					this.$router.push({ path: '/login' });
				}
				this.users = res.data.networks;
				this.listLoading = false;
				//NProgress.done();
			}).catch(() => {
				this.listLoading = false;
				this.$router.push({ path: '/login' });
			});
		},
		//删除
		handleDel: function(index, row) {
			this.$confirm('确认删除该记录吗?', '提示', {
				type: 'warning'
			}).then(() => {
				this.listLoading = true;
				//NProgress.start();
				let para = { id: row.id };
				// removeUser(para).then((res) => {
				this.$http.get('/api/remove_server/' + row.id).then((res) => {
					this.listLoading = false;
					//NProgress.done();
					this.$message({
						message: '删除成功',
						type: 'success'
					});
					this.getUsers();
				});
			}).catch(() => {
				this.$router.push({ path: '/login' });
			});
		},
		//显示编辑界面
		handleEdit: function(index, row) {
			this.editFormVisible = true;
			this.editForm = Object.assign({}, row);
			console.log(this.editForm.id)
			console.log(this.editForm.name)
		},
		//显示新增界面
		handleAdd: function() {
			this.$http.get('/api/show_create_instance/').then((res) => {
				console.log(res)
				this.image = res.data.images
				this.AZ = res.data.availabilityZoneInfo
				this.flavor = res.data.flavors
				this.network = res.data.networks
			})
			this.addFormVisible = true;
			this.addForm = {
				name: '',
				afin: [],
				affn: '',
				afnn: '',
				afan: '',
			};
		},
		//编辑
		editSubmit: function() {
			this.$refs.editForm.validate((valid) => {
				if (valid) {
					this.$confirm('确认提交吗？', '提示', {}).then(() => {
						this.editLoading = true;
						//NProgress.start();
						let para = Object.assign({}, this.editForm);
						// para.birth = (!para.birth || para.birth == '') ? '' : util.formatDate.format(new Date(para.birth), 'yyyy-MM-dd');
						// this.$http.post("/api/update_server/", para).then((res) => {
						this.$http.get("/api/update_server/" + this.editForm.name + '/' + this.editForm.id).then((res) => {
							this.editLoading = false;
							console.log(res)
							//NProgress.done();
							this.$message({
								message: '提交成功',
								type: 'success'
							});
							this.$refs['editForm'].resetFields();
							this.editFormVisible = false;
							this.getUsers();
						});
					}).catch(() => {
						this.$router.push({ path: '/login' });
					});
				}
			});
		},
		//新增
		addSubmit: function() {
			console.log(this.addForm)
			this.$refs.addForm.validate((valid) => {
				if (valid) {
					this.$confirm('确认提交吗？', '提示', {}).then(() => {
						this.addLoading = true;
						//NProgress.start();
						let para = Object.assign({}, this.addForm);
						para.birth = (!para.birth || para.birth == '') ? '' : util.formatDate.format(new Date(para.birth), 'yyyy-MM-dd');
						// addUser(para).then((res) => {
						this.$http.get('/api/create_server/' + this.addForm.afin.id + '/' + this.addForm.affn + '/' + this.addForm.afnn + '/' + this.addForm.afan + '/' + this.addForm.name).then((res) => {
							this.addLoading = false;
							console.log(res)
							//NProgress.done();
							this.$message({
								message: '提交成功',
								type: 'success'
							});
							this.$refs['addForm'].resetFields();
							this.addFormVisible = false;
							this.getUsers();
						});
					}).catch(() => {
						this.$router.push({ path: '/login' });
					});
				}
			});
		},
		selsChange: function(sels) {
			this.sels = sels;
		},
		//批量删除
		batchRemove: function() {
			var ids = this.sels.map(item => item.id).toString();
			this.$confirm('确认删除选中记录吗？', '提示', {
				type: 'warning'
			}).then(() => {
				this.listLoading = true;
				//NProgress.start();
				let para = { ids: ids };
				batchRemoveUser(para).then((res) => {
					this.listLoading = false;
					//NProgress.done();
					this.$message({
						message: '删除成功',
						type: 'success'
					});
					this.getUsers();
				});
			}).catch(() => {
				this.$router.push({ path: '/login' });
			});
		}
	},
	mounted() {
		this.getUsers();
	},
	ready: function() {
		setInterval(function() {
			this.getUsers();
		}.bind(this), 3000);
	},
	beforeDestroy: function() {
		clearInterval(this.interval);
	}
}

</script>

<style scoped>

</style>