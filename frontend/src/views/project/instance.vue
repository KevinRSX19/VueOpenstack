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
				<el-button type="danger" @click="batchRemove" :disabled="this.sels.length===0">批量删除</el-button>
				<el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="20" :total="total" style="float:right;">
				</el-pagination>
			</el-form>
		</el-col>
		<!--列表-->
		<el-table :data="users" highlight-current-row @current-change="currChange" v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
			<el-table-column type="selection">
			</el-table-column>
			<el-table-column type="index">
			</el-table-column>
			<el-table-column prop="name" label="实例名称" sortable>
				<template scope="scope">
					<el-button type="text" @click="handleDetail(scope.$index, scope.row)">{{ scope.row.name }}</el-button>
				</template>
			</el-table-column>
			<el-table-column prop="image.name" label="镜像" sortable>
			</el-table-column>
			<el-table-column prop="OS-EXT-AZ:availability_zone" label="可用域" sortable>
			</el-table-column>
			<el-table-column label="IP" sortable>
				<template scope="scope">
					<li style="list-style-type:none;" v-for="a in scope.row.addresses.public" :key="a.addr">{{a.addr}}</li>
				</template>
			</el-table-column>
			<el-table-column prop="flavor.id" label="实例类型" sortable>
			</el-table-column>
			<el-table-column prop="status" label="状态" sortable>
			</el-table-column>
			<el-table-column label="操作" min-width="100">
				<template scope="scope">
					<el-button-group>
						<el-button size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
					</el-button-group>
					<el-dropdown split-button size="small" @command="handleCommand" type="primary" trigger="click" @click="handleClick(scope.row)">
						制作镜像
						<el-dropdown-menu slot="dropdown">
							<el-dropdown-item v-for="l in btnlist_r" v-if="scope.row.status=='ACTIVE'" :key="l.key" :command="l.key">{{l.value}}</el-dropdown-item>
							<el-dropdown-item v-for="l in btnlist_p" v-if="scope.row.status=='PAUSED'" :key="l.key" :command="l.key">{{l.value}}</el-dropdown-item>
						</el-dropdown-menu>
					</el-dropdown>
				</template>
			</el-table-column>
		</el-table>
		<br>
		<el-tabs type="border-card">
			<el-tab-pane label="虚拟机硬盘">
				<el-table :data="vm_vol" highlight-current-row v-loading="loading" style="width: 100%;" :empty-text="vmvol">
					<el-table-column type="index">
					</el-table-column>
					<el-table-column prop="volumeId" label="名称" sortable>
					</el-table-column>
					<el-table-column prop="volume.size" label="容量(GB)" sortable>
					</el-table-column>
					<el-table-column prop="device" label="附加到" sortable>
					</el-table-column>
					<el-table-column prop="addr" label="操作" min-width="100" sortable>
						<template scope="scope">
							<el-button-group>
								<el-button type="primary" size="small" @click="handlePause(scope.$index, scope.row)">挂载</el-button>
								<el-button type="warning" size="small" @click="handleEdit(scope.$index, scope.row)">分离</el-button>
								<el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>
							</el-button-group>
						</template>
					</el-table-column>
				</el-table>
			</el-tab-pane>
			<el-tab-pane label="虚拟机网络">
				<el-table :data="vm_net" :empty-text="vmnet" highlight-current-row v-loading="listLoading" style="width: 100%;">
					<el-table-column type="index">
					</el-table-column>
					<el-table-column prop="name" label="名称" sortable>
					</el-table-column>
					<el-table-column prop="mac_addr" label="MAC" sortable>
					</el-table-column>
					<el-table-column prop="shared" label="IP" sortable>
					</el-table-column>
					<el-table-column prop="external" label="已连接网络" sortable>
					</el-table-column>
					<el-table-column prop="port_state" label="状态" sortable>
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
			</el-tab-pane>
		</el-tabs>

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

export default {
	data() {
		return {
			vmvol: '请选中一个虚拟机来查看其虚拟硬盘信息',
			vmnet: '请选中一个虚拟机来查看其网络信息',
			vm_vol: [],
			vm_net: [],
			btnlist_r: [{ value: '编辑', key: 'edit' },
			{ value: '暂停', key: 'pause' },
			{ value: '关机', key: 'stop' },
			{ value: '重启', key: 'restart' },
			{ value: '删除', key: 'delete' }],
			btnlist_p: [{ value: '恢复', key: 'unpause' },
			{ value: '删除', key: 'delete' }],
			instance_id: '',
			filters: {
				name: ''
			},
			users: [],
			total: 0,
			page: 1,
			listLoading: false,
			loading: false,
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
			AZ: [],
			activeName: 'second',
			intervalid1: ''

		}
	},
	methods: {
		handleClick(tab, event) {
			console.log(tab, event);
		},
		handleCurrentChange(val) {
			this.page = val;
			this.getUsers();
		},
		handleImageCurrentChange(val) {
			this.addForm.afin = val;
		},
		//获取用户列表
		getUsers() {
			console.log('getting users now')
			let para = {
				page: this.page,
				name: this.filters.name
			};
			this.listLoading = true;

			this.$http.get('/api/serverlist/').then((res) => {
				console.log(res.data);
				if (res.data == 'session expire') {
					this.$router.push({ path: '/login' });
				}
				this.users = res.data.servers;
				this.listLoading = false;
			}).catch(() => {
				this.$router.push({ path: '/login' });
			});
		},
		refreshUsers() {
			let para = {
				page: this.page,
				name: this.filters.name
			};
			this.$http.get('/api/serverlist/').then((res) => {
				console.log(res.data);
				if (res.data == 'session expire') {
					this.$router.push({ path: '/login' });
				}
				this.users = res.data.servers;
			}).catch(() => {
				this.$router.push({ path: '/login' });
			});
		},
		//删除
		handleDel: function(id) {
			this.$confirm('确认删除该记录吗?', '提示', {
				type: 'warning'
			}).then(() => {
				this.listLoading = true;
				let para = { id: id };
				this.$http.get('/api/remove_server/' + id).then((res) => {
					this.listLoading = false;
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
		//跳转详细信息
		handleDetail: function(index, row) {
			// console.log(index)
			console.log(row.name)
		},
		//暂停虚拟机
		handlePause: function(index, row) {
			// console.log(index)
			console.log(row.id)
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
						let para = Object.assign({}, this.editForm);
						this.$http.get("/api/update_server/" + this.editForm.name + '/' + this.editForm.id).then((res) => {
							this.editLoading = false;
							console.log(res)
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
						let para = Object.assign({}, this.addForm);
						this.$http.get('/api/create_server/' + this.addForm.afin.id + '/' + this.addForm.affn + '/' + this.addForm.afnn + '/' + this.addForm.afan + '/' + this.addForm.name).then((res) => {
							this.addLoading = false;
							console.log(res)
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
			console.log(sels)
			this.sels = sels;
		},
		currChange: function(curr) {
			console.log(curr.id)
			// this.sels = sels;
			this.instance_id = curr.id;
			this.$http.get('/api/detail/' + curr.id + '/').then((res) => {
				console.log(res.data)
				this.vm_vol=res.data.volumeAttachments
			})
		},
		//批量删除
		batchRemove: function() {
			var ids = this.sels.map(item => item.id).toString();
			this.$confirm('确认删除选中记录吗？', '提示', {
				type: 'warning'
			}).then(() => {
				this.listLoading = true;
				let para = { ids: ids };
				this.$http.post('/api/batchRemove/', para).then((res) => {
					this.listLoading = false;
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
		handleClick: function(row) {
			console.log('row')
		},
		handleCommand: function(comm) {
			console.log(comm)
			console.log(this.instance_id)
			if (comm === "delete") {
				console.log('dropdown delete')
				this.handleDel(this.instance_id)
			} else if (comm === "edit") {
				console.log('dropdown edit')
				this.handleEdit(this.instance_id)
			}
			else {
				this.$http.get('/api/actions?command=' + comm + '&id=' + this.instance_id).then((res) => {
					console.log(res)
					// this.getUsers();
					this.$notify({
						title: '成功',
						message: res.data,
						type: 'success'
					});
				}).catch(() => {
					this.$router.push({ path: '/login' });
				});
			}
		}
	},
	mounted() {
		this.getUsers();
	},
	created () {
      this.intervalid1 = setInterval(() => {
        this.refreshUsers();
      }, 10000)
    },beforeDestroy () {
      clearInterval(this.intervalid1)
    }
}

</script>

<style scoped>

</style>