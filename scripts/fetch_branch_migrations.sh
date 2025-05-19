
#!/bin/bash

HERE=$(dirname $(readlink -f "$0"))
ROOT=$(realpath $HERE/..)
BRANCH=$1

set -x

rm -fr $ROOT/apps/address/migrations/
rm -fr $ROOT/apps/accounts/migrations/
rm -fr $ROOT/apps/permission/migrations/
rm -fr $ROOT/apps/company/migrations/
rm -fr $ROOT/apps/client/migrations/
rm -fr $ROOT/apps/bidding/migrations/
rm -fr $ROOT/apps/supplier/migrations/
rm -fr $ROOT/apps/product/migrations/
rm -fr $ROOT/apps/transport/migrations/
rm -fr $ROOT/apps/contact/migrations/
rm -fr $ROOT/apps/order/migrations/
rm -fr $ROOT/apps/messager/migrations/
rm -fr $ROOT/apps/contract/migrations/
rm -fr $ROOT/apps/pncp/migrations/

git checkout $BRANCH -- $ROOT/apps/address/migrations/
git checkout $BRANCH -- $ROOT/apps/accounts/migrations/
git checkout $BRANCH -- $ROOT/apps/permission/migrations/
git checkout $BRANCH -- $ROOT/apps/company/migrations/
git checkout $BRANCH -- $ROOT/apps/client/migrations/
git checkout $BRANCH -- $ROOT/apps/bidding/migrations/
git checkout $BRANCH -- $ROOT/apps/supplier/migrations/
git checkout $BRANCH -- $ROOT/apps/product/migrations/
git checkout $BRANCH -- $ROOT/apps/transport/migrations/
git checkout $BRANCH -- $ROOT/apps/contact/migrations/
git checkout $BRANCH -- $ROOT/apps/order/migrations/
git checkout $BRANCH -- $ROOT/apps/messager/migrations/
git checkout $BRANCH -- $ROOT/apps/contract/migrations/
git checkout $BRANCH -- $ROOT/apps/pncp/migrations/
