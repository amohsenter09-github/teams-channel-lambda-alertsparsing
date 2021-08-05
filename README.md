# EventBridge Template

## AWS Cloud Development Kit (AWS CDK)

[Developer Guide](https://docs.aws.amazon.com/cdk/latest/guide) |
[CDK Workshop](https://cdkworkshop.com/) |
[Getting Started](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html) |
[API Reference](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-construct-library.html) |
[Examples](https://github.com/aws-samples/aws-cdk-examples) |

The **AWS Cloud Development Kit (AWS CDK)** is an open-source software development
framework to define cloud infrastructure in code and provision it through AWS CloudFormation.
It offers a high-level object-oriented abstraction to define AWS resources imperatively using
the power of modern programming languages.

Developers use the [CDK framework] to define reusable cloud components called [constructs],
which are composed together into [stacks], forming a "CDK app".

[cdk framework]: https://docs.aws.amazon.com/cdk/api/latest/
[constructs]: https://docs.aws.amazon.com/cdk/latest/guide/constructs.html
[stacks]: https://docs.aws.amazon.com/cdk/latest/guide/apps_and_stacks.html#stacks

## Create a Project & Setup

Clone & create a project under the appropriate groups.

### EventBridge initial setup

To perform an initial EventBridge setup, please change the following part in `cdk.json` accordingly the description below.

```javascript
{
    ...
    "props": {
      "serviceName": "ps-template-bus",
      "psExtensions": {
        "serviceOwnership": "Platform",
        "ownerEmail": "platform.microservices@burberry.com",
        "jiraKeyspace": "PLAT",
        "budgetProject": "PS"
      },
    },
}
```

Fields description:

- serviceName - name of a service and Event Bus name in AWS
- serviceOwnership - used for tagging, means belonging to [Microservices Capability Map](https://burberry.atlassian.net/wiki/spaces/TEx/pages/945750378/Microservices+Capability+Map)
- jiraKeyspace - used for tagging and Jira tickets creation, identifies the Jira project which a particular resource was created for (MUST be valid Jira keyspace). In addition, a SAST Jira issue type MUST be in this Jira Keyspace for Snyk Lifecycle
- ownerEmail - used for tagging, identifies who is responsible for the resource (e.g. email DL of some particular API Team)
- budgetProject - used for tagging, for now the constant `PS` have to be always used

### CI/CD Configuration in Gitlab

The following steps are necessary to set up CI/CD process in Gitlab

The CI/CD (aka [Software Factory](https://burberry.atlassian.net/wiki/spaces/TEx/pages/378077368/Software+Factory)) process is defined below.

- Following Setting MUST be Enabled
  - Merge Request Settings | _Settings-> General->Merge Request Settings_
    - Fast-forward Merge
    - Only Allow Merge Requests to be Merged if the Pipeline Succeeds
    - Only allow merge requests to be merged if all discussions are resolved
    - Show link to create/view merge request when pushing from the command line
  - Protected Tags Settings | _Settings-> Repository->Protected Tags_
    - Limit access to creating and updating any (`*`) tags only by Maintainers.

### Branching Strategy

One of the simplest Branching Strategy is used for developing a service:

- Only `feature` and `master` branches are used
- A new `feature branch` created from `master` for any code change (new feature, hotfix, refactoring etc.)
- [Commit Message Conventions](#commit-message-conventions) has to be followed during development
- When the code change is ready `feature branch` merged to `master` via Merge Request.
  **NOTE:** Only Fast-forward merge is allowed
- A release candidate is created in `master` and [Version Management](#Version-Management) put corresponding `tag`
- The release candidate is deployed on Preprod and Prod Environments

### CI/CD Pipeline Stages

- A commit push into `origin` will trigger the build & deploy to Dynamic ([Development Environment](#Multi-dev-environment))
- A `Merge Request` needs to be open once the build & deploy to Dynamic has succeeded and feature is ready for release
- A merge into `master` will trigger [Semantic-release](#Version-Management) processing to create a release candidate and put corresponding `tag`.
  **NOTE:** [Commit Message Conventions](#commit-message-conventions) has to be followed during development
- Putting a `tag` will trigger the build & deploy to Staging (Preprod Environment)
- A manual trigger is required to deploy a Release candidate to Production Environment

### Multi-dev environment

Gitlab Review Apps are set up to simplify parallel development.

- A new independent AWS environment for a particular service is created for any new feature branch at Gitlab.
- Full cleaning of AWS environment is triggered by the feature branch deletion or manual stop of a particular `Gitlab Environment`.

### Version Management

The service is semantically versioned (MAJOR.MINOR.PATCH). CI/CD pipeline uses [Semantic-release](https://github.com/semantic-release/semantic-release) NPM module, fully automated version management and package publishing.

Semantic-release uses the commit messages to determine the type of changes in the codebase. Following [formalized conventions for commit messages](https://gist.github.com/stephenparish/9941e89d80e2bc58a153) (in our case AngularJS), semantic-release automatically determines the next semantic version number, generates a changelog and publishes the release.

### Commit Message Conventions

To guarantee that Semantic-release will manage to determine the next semantic version number and hence to build release candidate, a developer MUST follow at least the simplest format of the commit message like "`<type>: <subject>`".

`<type>` determines a type of code changes in a particular commit. The following type are defined:

- **feat:** a new feature. Corresponds to Minor release (0.1.0)
- **fix:** a bug fix. Corresponds to Patch release (0.0.1)
- **docs:** documentation only changes. Doesn't trigger any release (0.0.0)
- **style:** changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc). Doesn't trigger any release (0.0.0)
- **refactor:** a code change that neither fixes a bug nor adds a feature. Doesn't trigger any release (0.0.0)
- **test:** adding missing tests or correcting existing tests. Doesn't trigger any release (0.0.0)
- **chore:** some maintenance changes (ci/cd flow, version in package.json etc.). Doesn't trigger any release (0.0.0)

In addition three extra types were configured to simplify semantic version manipulation:

- **patch:** corresponds to Patch release (0.0.1)
- **minor:** corresponds to Minor release (0.1.0)
- **major:** corresponds to Major release (1.0.0)

`<subject>` is just an informative commit message

**NOTE:** If you tick `Squash commits` in a Merge Request, the name of Merge Request MUST correspond to the format of the commit message `<type>: <subject>` as well.

## Project Structure

The following files MUST not be changed

- gitlab-ci.yaml (CI/CD file)

## Quality checks

To keep permanent quality of code, the following settings were done in the current template

### Git Hook: Pre-Commit

- This hook was set up to run eslint checks and unit tests. It takes no parameters, and is invoked before obtaining the proposed commit log message and making a commit.
- Exiting with a non-zero status from this script causes the `git commit` command to abort before creating a commit.
- In case of strong necessity it can be bypassed with the `--no-verify` option.
