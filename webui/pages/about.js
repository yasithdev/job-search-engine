import PageContainer from '../components/PageContainer';
import Link from 'next/link'

const Page = () => (
    <PageContainer>
        <h5>Job Search Engine</h5>
        <h6>Version 1.0.0</h6>
        <p>Compare with <Link href="https://cse.google.com/cse?cx=011774890396222229159:paktbcelgau"><a target="_blank">Google Custom Search</a></Link></p>
    </PageContainer>
)

export default Page