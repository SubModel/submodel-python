# Projects

A submodel project is a single folder that contains all the files needed to create and run a serverless worker.

## Convert existing worker to a project

If you already have a worker, you can convert it to a project by navigating to the root of the worker folder and running `submodel project new --init`.

You may need to update the default configuration within `submodel.toml` to match your project structure.

## Ignore Files and Folders

Create a `.submodelignore` file in the root of your project to ignore files and folders from being uploaded to the submodel platform, the same file will also be used to ignore files that should not trigger an API server reload.
