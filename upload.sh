find data/json/ -type f -exec gzip -9 -n {} \; -exec mv {}.gz {} \;
aws s3 sync . s3://duhaime/apps/umap-zoo --profile default --metadata-directive='REPLACE' --acl public-read
aws s3 cp data/json s3://duhaime/apps/umap-zoo/data/json --profile default --metadata-directive='REPLACE' --content-encoding 'gzip' --acl public-read --recursive
