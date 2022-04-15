use bimfit;

select * from user;
select * from `order`;
select * from `share`;
select * from message;
select * from chineseaddress;

-- login 界面填写邮箱，查询邮箱作为验证
select email from user;
select userId from user where email='213and215@qq.com' and password='123456';
select username from user where userId=1;

select orderId, username as decoratorName, response, `status`, bimModelFilePath
from `order`, `user`
where `order`.userId = 1 and `order`.decoratorId = `user`.userId;

delete from `order` where orderId = 13;
update `order` set status = 1 where orderId = 19;

select orderId, username as decoratorName, `describe`, response, `status`, bimModelFilePath, buildingName, `version`, addProvince, addCity, addCounty, addDetails from `order`, `user` where `order`.userId = 1 and `order`.orderId = 1 and `order`.decoratorId = `user`.userId;

select username, userId from `user` where role = 2;

-- 选择地址
select distinct province from chineseaddress;
select distinct city from chineseaddress where province = "湖北省";
select distinct county from chineseaddress where province = "湖北省" and city = "武汉市";

--  提交
INSERT INTO `order` (`userId`, `decoratorId`, `version`, `describe`, `status`, `bimModelFilePath`, `buildingName`, `addProvince`, `addCity`, `addCounty`, `addDetails`) VALUES ('1', '7', 'V1.1', '设计室内装修时，家具、饰品的摆设一定要整齐，这样看起来装修效果更佳，使室内空间更加舒适得当。空间的设计一定要合理，这样才能看出整体效果的好坏，要注重通风效果要好，视野要开阔。走廊、玄关等不能太大，避免造成空间的浪费。人们都喜欢天然美景，都喜欢阳光能直射室内，这样室内更加的透气，消除了室内的漆黑感，使室内色彩光芒，给人一种温暖的感觉。', '2', 'static\\img\\BIM.png', '商品房', '湖北省', '武汉市', '洪山区', '华中科技大学紫菘公寓7栋777');

select shareId, senderId, username, `role`, content, `share`.create_time from `share`,`user` where `user`.userId = senderId order by `share`.create_time desc;

select username, `role`, content, `share`.create_time, remarks, shareId from `share`,`user` where `user`.userId = senderId and shareId = 4 and senderId = 2;

select username from `user` where userId = 1;

update `share` set remarks = '{"remarks": [[2, "这个装修可以"], [4, "老铁666"]]}' where shareId = 4;

select * from message where senderId = 1 or receiverId = 1 order by sendTime desc;

select * from message where (senderId,receiverId) = (2, 3) or (senderId,receiverId) = (3, 2) ;
