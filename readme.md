__SDSS数据集下载及标签制作指南__
===
sdss公开数据集[dr17](http://skyserver.sdss.org/dr17/)
---
使用[casJob](http://skyserver.sdss.org/CasJobs/SubmitJob.aspx)来查询符合要求的数据
---
>恒星数据获取

```sql
-- Stars selected using Field criteria.
-- Give me the PSF colors of all stars brighter than g=20 that have PSP_STATUS = 2.
-- Another simple multi-table query.

SELECT TOP 1000
  s.psfMag_g,       -- or whatever you want from each object
  s.run,
  s.camCol,
  s.rerun,
  s.field
FROM Star s
     JOIN Field f ON s.fieldID = f.fieldID
WHERE 
  s.psfMag_g < 20 
  and  f.pspStatus = 2
```

>星系数据获取
```sql
-- Galaxies meeting two simple criteria. 
-- Find all galaxies brighter than r magnitude 22, where the local
-- extinction is > 0.175.  This is a simple query that uses a WHERE clause,
-- but now two conditions that must be met simultaneously.

SELECT TOP 10 objID 
FROM Galaxy 
WHERE 
  r < 22			-- r IS NOT deredenned
  and extinction_r > 0.175	-- extinction more than 0.175
```

>类星体数据获取
```sql
-- Find quasars in imaging data.
-- as specified by Xiaohui Fan et.al.
-- A rather straightforward query, just with many conditions.

SELECT TOP 100 run,         
  camCol,         
  rerun,         
  field,         
  objID,         
  u, g, r, i, z,
  ra, dec
FROM Star                                         -- or Galaxy
WHERE ( u - g > 2.0  or  u > 22.3 ) 
  and ( i < 19 ) 
  and ( i > 0 )
  and ( g - r > 1.0 )
  and ( r - i <
          (0.08 + 0.42 * (g - r - 0.96) )
    or    g - r > 2.26 )
  and ( i - z < 0.25 )

```

代码使用流程
---
将casJob的查询结果保存为csv文件备用

*1. python3 download_sdss_file.py*




*2. python3 gen_qso_list.py*

