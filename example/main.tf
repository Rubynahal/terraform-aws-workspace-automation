locals {
  subnet_a                         = module.vpc.subnet_1
  subnet_b                         = module.vpc.subnet_2
  directory_id_abc                 = "d-906sdd86f5e"
  directory_id_def                 = "d-sdfddd86f5e"
  directory_id_ghi                 = "d-sssgfd86f5e"
  directory_id_jkl                 = "d-rrhhfff6f5e"
  custom_security_group_id         = "sg-w3e5r23swdfserwr"

  tags = {
    owner = "rubynahal"
    project = "workspaces"
  }

}
## Directory registration

resource "aws_workspaces_directory" "directory_abc" {
  directory_id = local.directory_id_abc
  subnet_ids = [
    local.subnet_a,
    local.subnet_b
  ]

  tags = local.tags

  self_service_permissions {
    change_compute_type  = false
    increase_volume_size = false
    rebuild_workspace    = false
    restart_workspace    = true
    switch_running_mode  = false
  }

  workspace_access_properties {
    device_type_android    = "ALLOW"
    device_type_chromeos   = "ALLOW"
    device_type_ios        = "ALLOW"
    device_type_osx        = "ALLOW"
    device_type_web        = "ALLOW"
    device_type_windows    = "ALLOW"
    device_type_zeroclient = "ALLOW"
  }

  workspace_creation_properties {
    enable_internet_access              = false
    enable_maintenance_mode             = true
    user_enabled_as_local_administrator = true
    custom_security_group_id            = local.custom_security_group_id
  }

}

resource "aws_workspaces_directory" "directory_def" {
  directory_id = local.directory_id_def
  subnet_ids = [
   local.subnet_a,
   local.subnet_b
  ]

  tags = local.tags

  self_service_permissions {
    change_compute_type  = false
    increase_volume_size = false
    rebuild_workspace    = false
    restart_workspace    = true
    switch_running_mode  = false
  }

  workspace_access_properties {
    device_type_android    = "ALLOW"
    device_type_chromeos   = "ALLOW"
    device_type_ios        = "ALLOW"
    device_type_osx        = "ALLOW"
    device_type_web        = "ALLOW"
    device_type_windows    = "ALLOW"
    device_type_zeroclient = "ALLOW"
  }

  workspace_creation_properties {
    enable_internet_access              = false
    enable_maintenance_mode             = true
    user_enabled_as_local_administrator = true
    default_ou                          = "OU=Workspaces,DC=def,DC=net,DC=somedomain,DC=internal"
  }

}

resource "aws_workspaces_directory" "directory_ghi" {
  directory_id = local.directory_id_ghi
  subnet_ids = [
    local.subnet_a,
    local.subnet_b
  ]

  tags = local.tags

  self_service_permissions {
    change_compute_type  = false
    increase_volume_size = false
    rebuild_workspace    = false
    restart_workspace    = true
    switch_running_mode  = false
  }

  workspace_access_properties {
    device_type_android    = "ALLOW"
    device_type_chromeos   = "ALLOW"
    device_type_ios        = "ALLOW"
    device_type_osx        = "ALLOW"
    device_type_web        = "ALLOW"
    device_type_windows    = "ALLOW"
    device_type_zeroclient = "ALLOW"
  }

  workspace_creation_properties {
    enable_internet_access              = false
    enable_maintenance_mode             = true
    user_enabled_as_local_administrator = true
  }

}

resource "aws_workspaces_directory" "directory_jkl" {
  directory_id = local.directory_id_jkl
  subnet_ids = [
    local.subnet_a,
    local.subnet_b
  ]

  tags = local.tags

  self_service_permissions {
    change_compute_type  = false
    increase_volume_size = false
    rebuild_workspace    = false
    restart_workspace    = true
    switch_running_mode  = false
  }

  workspace_access_properties {
    device_type_android    = "ALLOW"
    device_type_chromeos   = "ALLOW"
    device_type_ios        = "ALLOW"
    device_type_osx        = "ALLOW"
    device_type_web        = "ALLOW"
    device_type_windows    = "ALLOW"
    device_type_zeroclient = "ALLOW"
  }

  workspace_creation_properties {
    enable_internet_access              = false
    enable_maintenance_mode             = true
    user_enabled_as_local_administrator = true
  }

}

module "workspace_manager" {
  source = "./modules/workspace-manager"
  vpc_security_group_ids = [var.lambda_security_group]
  vpc_subnet_ids         = [var.subnet_a, var.subnet_b]
  function_name = "workspace-manager"
  description   = "This Lambda add or remove WorkSpaces based on CSV"
  handler = "lambda_function.lambda_handler"
  runtime = "python3.8"
  lambda_kms_key_arn = var.managed_lambda_key
  cloudwatch_kms_key_arn = var.managed_cloudwatch_log_kms_key
  cloudwatch_logs_retention_in_days = "7"
  tracing_mode = "Active"
  abc_dir_id               = var.directory_id_abc
  def_dir_id               = var.directory_id_def
  ghi_dir_id               = var.directory_id_ghi
  jkl_dir_id               = var.directory_id_jkl
  win_perf_bundle_id       = var.bundle_id_win_perf
  win_gpu_bundle_id        = var.bundle_id_win_gpu
  linux_perf_bundle_id     = var.bundle_id_linux_perf
  linux_powerpro_bundle_id = var.bundle_id_linux_powerpro
  workspaces_kms_key       = aws_kms_key.workspace_kms_key.arn
  source_bucket            = var.s3_bucket_name
  tags = local.tags
}

resource "aws_kms_key" "workspace_kms_key" {
  description             = "managed-workspaces-key"
  enable_key_rotation     = true
  policy                  = <<EOT
{
  "Version": "2012-10-17",
  "Id": "aws-kms-key-policy",
  "Statement": [
        {
            "Sid": "SetupRolesAsKeyAdministrators",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::12345678900:role/OrganizationAccountAccessRole"
            },
            "Action": [
                "kms:Create*",
                "kms:Describe*",
                "kms:Enable*",
                "kms:List*",
                "kms:Put*",
                "kms:Update*",
                "kms:Revoke*",
                "kms:Disable*",
                "kms:Get*",
                "kms:Delete*",
                "kms:TagResource",
                "kms:UntagResource",
                "kms:ScheduleKeyDeletion",
                "kms:CancelKeyDeletion"
            ],
            "Resource": "*"
        },
        {
            "Sid": "AllowReadPermissions",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::12345678900:root"
            },
            "Action": [
                "kms:Describe*",
                "kms:Get*",
                "kms:List*"
            ],
            "Resource": "*"
        },
        {
            "Sid": "Allow access through Workspaces for all principals in the account that are authorized to use Workspaces",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": [
                "kms:Encrypt",
                "kms:Decrypt",
                "kms:ReEncrypt*",
                "kms:GenerateDataKey*",
                "kms:CreateGrant",
                "kms:ListGrants",
                "kms:DescribeKey"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "kms:CallerAccount": "12345678900",
                    "kms:ViaService": "workspaces.us-west-2.amazonaws.com"
                }
            }
        }
  ]
}
EOT
}

resource "aws_kms_alias" "workspace_kms_key_alias" {
  name          = "alias/managed-workspaces-key"
  target_key_id = aws_kms_key.workspace_kms_key.key_id
}
